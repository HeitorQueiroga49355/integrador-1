"""
Serviço para distribuição de submissões para avaliadores.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from evaluations.models import Reviewer, SubmissionAssignment, Evaluation
from submission.models import Submission
from proposals.models import Proposal
import random


class SubmissionDistributionService:
    """
    Serviço responsável por distribuir submissões para avaliadores.
    """
    
    def __init__(self, proposal):
        self.proposal = proposal
    
    def distribute_submissions(self, submissions_per_reviewer=3, reviewers_per_submission=2, assigned_by=None):
        """
        Distribui as submissões de um edital para os avaliadores.
        
        Args:
            submissions_per_reviewer: Número máximo de submissões por avaliador
            reviewers_per_submission: Número de avaliadores por submissão
            assigned_by: Usuário que está fazendo a distribuição
        
        Returns:
            dict: Estatísticas da distribuição
        """
        # Busca todas as submissões do edital
        submissions = Submission.objects.filter(proposal=self.proposal)
        
        # Busca todos os avaliadores disponíveis da mesma instituição
        reviewers = Reviewer.objects.filter(
            institution=self.proposal.institution
        )
        
        if not reviewers.exists():
            raise ValueError("Nenhum avaliador cadastrado para esta instituição")
        
        if not submissions.exists():
            raise ValueError("Nenhuma submissão encontrada para este edital")
        
        stats = {
            'total_submissions': submissions.count(),
            'total_reviewers': reviewers.count(),
            'assignments_created': 0,
            'evaluations_created': 0,
            'notifications_sent': 0,
            'errors': []
        }
        
        with transaction.atomic():
            # Para cada submissão, atribui avaliadores
            for submission in submissions:
                # Pega avaliadores que ainda não foram atribuídos a esta submissão
                existing_assignments = SubmissionAssignment.objects.filter(
                    submission=submission
                ).values_list('reviewer_id', flat=True)
                
                available_reviewers = reviewers.exclude(id__in=existing_assignments)
                
                # Seleciona avaliadores aleatoriamente (ou pode usar critério de expertise)
                selected_reviewers = self._select_reviewers(
                    available_reviewers,
                    reviewers_per_submission,
                    submission
                )
                
                # Cria as atribuições
                for reviewer in selected_reviewers:
                    try:
                        assignment = self._create_assignment(
                            submission,
                            reviewer,
                            assigned_by
                        )
                        stats['assignments_created'] += 1
                        
                        # Cria a avaliação vinculada
                        evaluation = self._create_evaluation(
                            assignment,
                            submission,
                            reviewer
                        )
                        stats['evaluations_created'] += 1
                        
                        # Notifica o avaliador
                        if self._notify_reviewer(reviewer, submission, assignment):
                            stats['notifications_sent'] += 1
                            
                    except Exception as e:
                        stats['errors'].append(f"Erro ao atribuir {reviewer.name}: {str(e)}")
        
        return stats
    
    def _select_reviewers(self, available_reviewers, count, submission):
        """
        Seleciona avaliadores para uma submissão.
        Pode ser expandido para usar critérios de expertise.
        """
        # Por enquanto, seleção aleatória
        reviewers_list = list(available_reviewers)
        
        if len(reviewers_list) < count:
            return reviewers_list
        
        return random.sample(reviewers_list, count)
    
    def _create_assignment(self, submission, reviewer, assigned_by):
        """
        Cria uma atribuição de submissão para avaliador.
        """
        assignment, created = SubmissionAssignment.objects.get_or_create(
            submission=submission,
            reviewer=reviewer,
            defaults={
                'assigned_by': assigned_by,
            }
        )
        return assignment
    
    def _create_evaluation(self, assignment, submission, reviewer):
        """
        Cria uma avaliação vazia vinculada à atribuição.
        """
        evaluation, created = Evaluation.objects.get_or_create(
            assignment=assignment,
            submission=submission,
            reviewer=reviewer,
            defaults={
                'institution': self.proposal.institution,
                'proposal': self.proposal,
                'status': 'pending'
            }
        )
        return evaluation
    
    def _notify_reviewer(self, reviewer, submission, assignment):
        """
        Notifica o avaliador por email sobre a nova atribuição.
        """
        try:
            subject = f"Nova submissão para avaliar: {submission.title}"
            message = f"""
Olá {reviewer.name},

Você foi designado(a) para avaliar a seguinte submissão:

Edital: {self.proposal.title}
Submissão: {submission.title}
Pesquisador: {submission.researcher.user.get_full_name()}

Por favor, acesse o sistema para realizar sua avaliação.

Atenciosamente,
Sistema de Gestão de Editais
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [reviewer.email],
                fail_silently=False,
            )
            
            # Marca como notificado
            assignment.notified = True
            assignment.notified_date = timezone.now()
            assignment.save()
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar email para {reviewer.email}: {str(e)}")
            return False
    
    def get_distribution_stats(self):
        """
        Retorna estatísticas da distribuição atual do edital.
        """
        submissions = Submission.objects.filter(proposal=self.proposal)
        
        stats = {
            'total_submissions': submissions.count(),
            'submissions_with_reviewers': 0,
            'total_assignments': 0,
            'pending_evaluations': 0,
            'completed_evaluations': 0,
            'reviewers_workload': {}
        }
        
        # Conta submissões com avaliadores
        for submission in submissions:
            assignment_count = SubmissionAssignment.objects.filter(
                submission=submission
            ).count()
            
            if assignment_count > 0:
                stats['submissions_with_reviewers'] += 1
            
            stats['total_assignments'] += assignment_count
        
        # Conta avaliações pendentes e concluídas
        stats['pending_evaluations'] = Evaluation.objects.filter(
            proposal=self.proposal,
            status__in=['pending', 'in_progress']
        ).count()
        
        stats['completed_evaluations'] = Evaluation.objects.filter(
            proposal=self.proposal,
            status='completed'
        ).count()
        
        # Carga de trabalho dos avaliadores
        reviewers = Reviewer.objects.filter(
            institution=self.proposal.institution
        )
        
        for reviewer in reviewers:
            assignment_count = SubmissionAssignment.objects.filter(
                reviewer=reviewer,
                submission__proposal=self.proposal
            ).count()
            
            if assignment_count > 0:
                stats['reviewers_workload'][reviewer.name] = {
                    'total_assignments': assignment_count,
                    'pending': Evaluation.objects.filter(
                        reviewer=reviewer,
                        proposal=self.proposal,
                        status__in=['pending', 'in_progress']
                    ).count(),
                    'completed': Evaluation.objects.filter(
                        reviewer=reviewer,
                        proposal=self.proposal,
                        status='completed'
                    ).count()
                }
        
        return stats


def auto_distribute_on_proposal_close(proposal_id, assigned_by=None):
    """
    Função auxiliar para ser chamada quando um edital for fechado.
    Pode ser usado em um signal ou task agendada.
    """
    try:
        proposal = Proposal.objects.get(id=proposal_id)
        
        # Verifica se o edital está fechado
        from datetime import date
        if proposal.closing_date >= date.today():
            return {
                'success': False,
                'message': 'Edital ainda não foi fechado'
            }
        
        # Verifica se já foi distribuído
        existing_assignments = SubmissionAssignment.objects.filter(
            submission__proposal=proposal
        ).exists()
        
        if existing_assignments:
            return {
                'success': False,
                'message': 'Este edital já possui distribuições'
            }
        
        # Distribui
        service = SubmissionDistributionService(proposal)
        stats = service.distribute_submissions(assigned_by=assigned_by)
        
        return {
            'success': True,
            'message': 'Distribuição realizada com sucesso',
            'stats': stats
        }
        
    except Proposal.DoesNotExist:
        return {
            'success': False,
            'message': 'Edital não encontrado'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Erro na distribuição: {str(e)}'
        }