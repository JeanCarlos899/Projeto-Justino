from django.views.generic import ListView
from .models import Question, Disciplina, Conteudo, Logo
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class ElaboradorApp:
    def __init__(self):
        self.disciplinas = Disciplina.objects.all()
        self.conteudos = Conteudo.objects.all()
        self.logos = Logo.objects.all()

    @login_required(login_url='/admin/')
    def index(request):
        return render(request, 'elaboradorapp/index.html', {
            'disciplinas': Disciplina.objects.all(),
            'conteudos': Conteudo.objects.all(),
            'logos': Logo.objects.all(),
        })


class ListarQuestoes(ListView):
    model = Question
    template_name = 'elaboradorapp/listar_questoes.html'

    def get_context_data(self, **kwargs):

        disciplina_escolhida = self.request.GET.get('disciplina')
        quantidade_questoes = self.request.GET.get('quantidade_questoes')
        conteudo_escolhido = self.request.GET.get('conteudo')
        segundo_conteudo = self.request.GET.get('segundo_conteudo')
        terceiro_conteudo = self.request.GET.get('terceiro_conteudo')
        serie_escolhida = self.request.GET.get('serie')
        dificuldade_escolhida = self.request.GET.get('dificuldade')
        nome_professor = self.request.GET.get('nome_professor')
        curso = self.request.GET.get('curso')
        turma = self.request.GET.get('turma')
        data = self.request.GET.get('data')
        observacao_1 = self.request.GET.get('observacao_1')
        observacao_2 = self.request.GET.get('observacao_2')
        observacao_3 = self.request.GET.get('observacao_3')
        nome_logo = self.request.GET.get('nome_logo')
        tipo_prova = self.request.GET.get('tipo_prova')
        bimestre = self.request.GET.get('bimestre')

        context = super().get_context_data(**kwargs)
        questoes = Question.objects.all()


        conteudo = Conteudo.objects.filter(nome=conteudo_escolhido).first()
        segundo_conteudo = Conteudo.objects.filter(nome=segundo_conteudo).first()
        terceiro_conteudo = Conteudo.objects.filter(nome=terceiro_conteudo).first()
        disciplina = Disciplina.objects.filter(nome=disciplina_escolhida).first()
        logo = Logo.objects.filter(nome=nome_logo).first().imagem.url

        if conteudo:
            conteudo = conteudo.pk
        if segundo_conteudo:
            segundo_conteudo = segundo_conteudo.pk
        if terceiro_conteudo:
            terceiro_conteudo = terceiro_conteudo.pk
        if disciplina:
            disciplina = disciplina.pk
        if data:
            data = datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')


        if serie_escolhida == 'Indefinido' and dificuldade_escolhida != 'Indefinido':
            qtd_conteudos = 1
            if segundo_conteudo:
                questoes_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    dificuldade=dificuldade_escolhida
                    )
                questoes_faceis_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    dificuldade='F'
                    )
                questoes_medias_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    dificuldade='M'
                    )
                questoes_dificeis_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    dificuldade='D'
                    )
                if dificuldade_escolhida == 'F':
                    questoes_segundo_conteudo = questoes_segundo_conteudo | questoes_medias_segundo_conteudo.order_by('?')[:int(len(questoes_medias_segundo_conteudo) * 0.5)]
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')
                if dificuldade_escolhida == 'M':
                    questoes_segundo_conteudo = questoes_segundo_conteudo | questoes_dificeis_segundo_conteudo.order_by('?')[:int(len(questoes_dificeis_segundo_conteudo) * 0.5)] | questoes_faceis_segundo_conteudo.order_by('?')[:int(len(questoes_faceis_segundo_conteudo) * 0.5)]
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')
                if dificuldade_escolhida == 'D':
                    questoes_segundo_conteudo = questoes_segundo_conteudo | questoes_medias_segundo_conteudo.order_by('?')[:int(len(questoes_medias_segundo_conteudo) * 0.5)]
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')
                qtd_conteudos += 1
            if terceiro_conteudo:
                questoes_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo,
                    dificuldade=dificuldade_escolhida
                    )
                questoes_faceis_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo,
                    dificuldade='F'
                    )
                questoes_medias_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo,
                    dificuldade='M'
                    )
                if dificuldade_escolhida == 'F':
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo | questoes_medias_terceiro_conteudo.order_by('?')[:int(len(questoes_medias_terceiro_conteudo) * 0.5)]
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')
                if dificuldade_escolhida == 'M':
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo | questoes_faceis_terceiro_conteudo.order_by('?')[:int(len(questoes_faceis_terceiro_conteudo) * 0.5)]
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')
                if dificuldade_escolhida == 'D':
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo | questoes_medias_terceiro_conteudo.order_by('?')[:int(len(questoes_medias_terceiro_conteudo) * 0.5)]
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')
                qtd_conteudos += 1

            questoes_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                dificuldade=dificuldade_escolhida
                )
            questoes_faceis_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                dificuldade='F'
                )
            questoes_medias_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                dificuldade='M'
                )
            questoes_dificeis_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                dificuldade='D'
                )
            if dificuldade_escolhida == 'F':
                questoes_primeiro_conteudo = questoes_primeiro_conteudo | questoes_medias_primeiro_conteudo.order_by('?')[:int(len(questoes_medias_primeiro_conteudo) * 0.5)]
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')
            if dificuldade_escolhida == 'M':
                questoes_primeiro_conteudo = questoes_primeiro_conteudo | questoes_dificeis_primeiro_conteudo.order_by('?')[:int(len(questoes_dificeis_primeiro_conteudo) * 0.5)] | questoes_faceis_primeiro_conteudo.order_by('?')[:int(len(questoes_faceis_primeiro_conteudo) * 0.5)]
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')
            if dificuldade_escolhida == 'D':
                questoes_primeiro_conteudo = questoes_primeiro_conteudo | questoes_medias_primeiro_conteudo.order_by('?')[:int(len(questoes_medias_primeiro_conteudo) * 0.5)]
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')

            if int(quantidade_questoes) % qtd_conteudos == 0:
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if segundo_conteudo:
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if terceiro_conteudo:
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
            else:
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos + 1]
                if segundo_conteudo:
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if terceiro_conteudo:
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]

            questoes = questoes_primeiro_conteudo
            if segundo_conteudo:
                questoes = questoes | questoes_segundo_conteudo
            if terceiro_conteudo:
                questoes = questoes | questoes_terceiro_conteudo

        if dificuldade_escolhida == 'Indefinido' and serie_escolhida != 'Indefinido':
            qtd_conteudos = 1
            if segundo_conteudo:
                questoes_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    serie=serie_escolhida
                    )
                qtd_conteudos += 1
            if terceiro_conteudo:
                questoes_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo,
                    serie=serie_escolhida
                    )
                qtd_conteudos += 1

            questoes_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                serie=serie_escolhida
                )

            if int(quantidade_questoes) % qtd_conteudos == 0:
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if segundo_conteudo:
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if terceiro_conteudo:
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
            else:
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos + 1]
                if segundo_conteudo:
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if terceiro_conteudo:
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]

            questoes = questoes_primeiro_conteudo
            if segundo_conteudo:
                questoes = questoes | questoes_segundo_conteudo
            if terceiro_conteudo:
                questoes = questoes | questoes_terceiro_conteudo

        if serie_escolhida == 'Indefinido' and dificuldade_escolhida == 'Indefinido':
            qtd_conteudos = 1
            if segundo_conteudo:
                questoes_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina, conteudo=segundo_conteudo
                    )
                qtd_conteudos += 1
            if terceiro_conteudo:
                questoes_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo
                    )
                qtd_conteudos += 1

            questoes_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo
                )

            if int(quantidade_questoes) % qtd_conteudos == 0:
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if segundo_conteudo:
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if terceiro_conteudo:
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
            else:
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos + 1]
                if segundo_conteudo:
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if terceiro_conteudo:
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]

            questoes = questoes_primeiro_conteudo
            if segundo_conteudo:
                questoes = questoes | questoes_segundo_conteudo
            if terceiro_conteudo:
                questoes = questoes | questoes_terceiro_conteudo

        if dificuldade_escolhida != 'Indefinido' and serie_escolhida != 'Indefinido':
            qtd_conteudos = 1
            if segundo_conteudo:
                questoes_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    serie=serie_escolhida,
                    dificuldade=dificuldade_escolhida
                    )
                questoes_faceis_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    serie=serie_escolhida,
                    dificuldade='F'
                    )
                questoes_medias_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    serie=serie_escolhida,
                    dificuldade='M'
                    )
                questoes_dificeis_segundo_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=segundo_conteudo,
                    serie=serie_escolhida,
                    dificuldade='D'
                    )
                if dificuldade_escolhida == 'F':
                    questoes_segundo_conteudo = questoes_segundo_conteudo | questoes_medias_segundo_conteudo.order_by('?')[:int(len(questoes_medias_segundo_conteudo) * 0.5)]
                if dificuldade_escolhida == 'M':
                    questoes_segundo_conteudo = questoes_segundo_conteudo | questoes_dificeis_segundo_conteudo.order_by('?')[:int(len(questoes_dificeis_segundo_conteudo) * 0.5)] | questoes_faceis_segundo_conteudo.order_by('?')[:int(len(questoes_faceis_segundo_conteudo) * 0.5)]
                if dificuldade_escolhida == 'D':
                    questoes_segundo_conteudo = questoes_segundo_conteudo | questoes_medias_segundo_conteudo.order_by('?')[:int(len(questoes_medias_segundo_conteudo) * 0.5)]

                qtd_conteudos += 1
            if terceiro_conteudo:
                questoes_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo,
                    serie=serie_escolhida,
                    dificuldade=dificuldade_escolhida
                    )
                qtd_conteudos += 1
                questoes_faceis_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo,
                    serie=serie_escolhida,
                    dificuldade='F'
                    )
                questoes_medias_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo,
                    serie=serie_escolhida,
                    dificuldade='M'
                    )
                questoes_dificeis_terceiro_conteudo = Question.objects.filter(
                    disciplina=disciplina,
                    conteudo=terceiro_conteudo,
                    serie=serie_escolhida,
                    dificuldade='D'
                    )
                if dificuldade_escolhida == 'F':
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo | questoes_medias_terceiro_conteudo.order_by('?')[:int(len(questoes_medias_terceiro_conteudo) * 0.5)]
                if dificuldade_escolhida == 'M':
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo | questoes_dificeis_terceiro_conteudo.order_by('?')[:int(len(questoes_dificeis_terceiro_conteudo) * 0.5)] | questoes_faceis_terceiro_conteudo.order_by('?')[:int(len(questoes_faceis_terceiro_conteudo) * 0.5)]
                if dificuldade_escolhida == 'D':
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo | questoes_medias_terceiro_conteudo.order_by('?')[:int(len(questoes_medias_terceiro_conteudo) * 0.5)]

            questoes_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                serie=serie_escolhida,
                dificuldade=dificuldade_escolhida
                )
            questoes_faceis_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                serie=serie_escolhida,
                dificuldade='F'
                )
            questoes_medias_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                serie=serie_escolhida,
                dificuldade='M'
                )
            questoes_dificeis_primeiro_conteudo = Question.objects.filter(
                disciplina=disciplina,
                conteudo=conteudo,
                serie=serie_escolhida,
                dificuldade='D'
                )
            if dificuldade_escolhida == 'F':
                questoes_primeiro_conteudo = questoes_primeiro_conteudo | questoes_medias_primeiro_conteudo.order_by('?')[:int(len(questoes_medias_primeiro_conteudo) * 0.5)]
            if dificuldade_escolhida == 'M':
                questoes_primeiro_conteudo = questoes_primeiro_conteudo | questoes_dificeis_primeiro_conteudo.order_by('?')[:int(len(questoes_dificeis_primeiro_conteudo) * 0.5)] | questoes_faceis_primeiro_conteudo.order_by('?')[:int(len(questoes_faceis_primeiro_conteudo) * 0.5)]
            if dificuldade_escolhida == 'D':
                questoes_primeiro_conteudo = questoes_primeiro_conteudo | questoes_medias_primeiro_conteudo.order_by('?')[:int(len(questoes_medias_primeiro_conteudo) * 0.5)]

            if int(quantidade_questoes) % qtd_conteudos == 0:
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if segundo_conteudo:
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if terceiro_conteudo:
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
            else:
                questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos + 1]
                if segundo_conteudo:
                    questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                if terceiro_conteudo:
                    questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]

            questoes = questoes_primeiro_conteudo
            if segundo_conteudo:
                questoes = questoes | questoes_segundo_conteudo
            if terceiro_conteudo:
                questoes = questoes | questoes_terceiro_conteudo

        context.update({
            'questoes': questoes,
            'nome_disciplina': disciplina_escolhida,
            'nome_conteudo': conteudo_escolhido,
            'nome_professor': nome_professor,
            'tipo_prova': tipo_prova,
            'observacao1': observacao_1,
            'observacao2': observacao_2,
            'observacao3': observacao_3,
            'curso': curso,
            'turma': turma,
            'data': data,
            'logo': logo,
            'bimestre': bimestre,
        })

        return context

class Sobre(ListView):
    model = Question
    template_name = 'elaboradorapp/sobre.html'


    




# from django.views.generic import ListView
# from .models import Question, Disciplina, Conteudo, Logo
# import datetime
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.db.models import Q

# class ElaboradorApp:
#     def __init__(self):
#         self.disciplinas = Disciplina.objects.all()
#         self.conteudos = Conteudo.objects.all()
#         self.logos = Logo.objects.all()

#     @login_required(login_url='/admin/')
#     def index(request):
#         return render(request, 'elaboradorapp/index.html', {
#             'disciplinas': Disciplina.objects.all(),
#             'conteudos': Conteudo.objects.all(),
#             'logos': Logo.objects.all(),
#         })

# class ListarQuestoes(ListView):
#     model = Question
#     template_name = 'elaboradorapp/listar_questoes.html'
    
#     def get_context_data(self, **kwargs):

#         disciplina_escolhida = self.request.GET.get('disciplina')
#         quantidade_questoes = self.request.GET.get('quantidade_questoes')
#         conteudo_escolhido = self.request.GET.get('conteudo')
#         segundo_conteudo = self.request.GET.get('segundo_conteudo')
#         terceiro_conteudo = self.request.GET.get('terceiro_conteudo')
#         serie_escolhida = self.request.GET.get('serie')
#         dificuldade_escolhida = self.request.GET.get('dificuldade')
#         nome_logo = self.request.GET.get('nome_logo')

#         context = super().get_context_data(**kwargs)
#         conteudo = Conteudo.objects.filter(nome=conteudo_escolhido).first() 
#         segundo_conteudo = Conteudo.objects.filter(nome=segundo_conteudo).first()
#         terceiro_conteudo = Conteudo.objects.filter(nome=terceiro_conteudo).first()
#         disciplina = Disciplina.objects.filter(nome=disciplina_escolhida).first()
#         logo = Logo.objects.filter(nome=nome_logo).first().imagem.url
        
#         if conteudo:
#             conteudo = conteudo.pk
#         if segundo_conteudo:
#             segundo_conteudo = segundo_conteudo.pk
#         if terceiro_conteudo:
#             terceiro_conteudo = terceiro_conteudo.pk
#         if disciplina:
#             disciplina = disciplina.pk

#         dictionary_questions = {
#             'primeiro_conteudo': Question.objects.filter(
#                 disciplina=disciplina, 
#                 conteudo=conteudo, 
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q(),
#                 Q(dificuldade=dificuldade_escolhida) if dificuldade_escolhida != 'Indefinido' else Q()
#             ),
#             'faceis_primeiro_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=conteudo,
#                 dificuldade='F'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#             'medias_primeiro_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=conteudo,
#                 dificuldade='M'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#             'dificeis_primeiro_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=conteudo,
#                 serie=serie_escolhida,
#                 dificuldade='D'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#             'segundo_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=segundo_conteudo,
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q(),
#                 Q(dificuldade=dificuldade_escolhida) if dificuldade_escolhida != 'Indefinido' else Q()
#             ),
#             'faceis_segundo_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=segundo_conteudo,
#                 dificuldade='F'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#             'medias_segundo_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=segundo_conteudo,
#                 dificuldade='M'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#             'dificeis_segundo_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=segundo_conteudo,
#                 dificuldade='D'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#             'terceiro_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=terceiro_conteudo,
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q(),
#                 Q(dificuldade=dificuldade_escolhida) if dificuldade_escolhida != 'Indefinido' else Q()
#             ),
#             'faceis_terceiro_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=terceiro_conteudo,
#                 dificuldade='F'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#             'medias_terceiro_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=terceiro_conteudo,
#                 dificuldade='M'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#             'dificeis_terceiro_conteudo': Question.objects.filter(
#                 disciplina=disciplina,
#                 conteudo=terceiro_conteudo,
#                 dificuldade='D'
#             ).filter(
#                 Q(serie=serie_escolhida) if serie_escolhida != 'Indefinido' else Q()
#             ),
#         }
        
#         questoes = None
#         questoes_segundo_conteudo = None
#         questoes_terceiro_conteudo = None

#         if serie_escolhida == 'Indefinido' and dificuldade_escolhida != 'Indefinido' or dificuldade_escolhida != 'Indefinido' and serie_escolhida != 'Indefinido':
#             qtd_conteudos = 0
#             if dictionary_questions['primeiro_conteudo']:
#                 if dificuldade_escolhida == 'F':
#                     questoes_primeiro_conteudo = dictionary_questions['primeiro_conteudo'] | dictionary_questions['medias_primeiro_conteudo'].order_by('?')[:int(len(dictionary_questions['medias_primeiro_conteudo']) * 0.5)]
#                     questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')
#                 if dificuldade_escolhida == 'M':
#                     questoes_primeiro_conteudo = dictionary_questions['primeiro_conteudo'] | dictionary_questions['dificeis_primeiro_conteudo'].order_by('?')[:int(len(dictionary_questions['dificeis_primeiro_conteudo']) * 0.5)] | dictionary_questions['faceis_primeiro_conteudo'].order_by('?')[:int(len(dictionary_questions['faceis_primeiro_conteudo']) * 0.5)]
#                     questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')
#                 if dificuldade_escolhida == 'D':
#                     questoes_primeiro_conteudo = dictionary_questions['primeiro_conteudo'] | dictionary_questions['medias_primeiro_conteudo'].order_by('?')[:int(len(dictionary_questions['medias_primeiro_conteudo']) * 0.5)]
#                     questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')
#                 qtd_conteudos += 1
            
#             if dictionary_questions['segundo_conteudo']:
#                 if dificuldade_escolhida == 'F':
#                     questoes_segundo_conteudo = dictionary_questions['segundo_conteudo'] | dictionary_questions['medias_segundo_conteudo'].order_by('?')[:int(len(dictionary_questions['medias_segundo_conteudo']) * 0.5)]
#                     questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')    
#                 if dificuldade_escolhida == 'M':
#                     questoes_segundo_conteudo = dictionary_questions['segundo_conteudo'] | dictionary_questions['dificeis_segundo_conteudo'].order_by('?')[:int(len(dictionary_questions['dificeis_segundo_conteudo']) * 0.5)] | dictionary_questions['faceis_segundo_conteudo'].order_by('?')[:int(len(dictionary_questions['faceis_segundo_conteudo']) * 0.5)]
#                     questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')    
#                 if dificuldade_escolhida == 'D':
#                     questoes_segundo_conteudo = dictionary_questions['segundo_conteudo'] | dictionary_questions['medias_segundo_conteudo'].order_by('?')[:int(len(dictionary_questions['medias_segundo_conteudo']) * 0.5)]
#                     questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')
#                 qtd_conteudos += 1

#             if dictionary_questions['terceiro_conteudo']:
#                 if dificuldade_escolhida == 'F':
#                     questoes_terceiro_conteudo = dictionary_questions['terceiro_conteudo'] | dictionary_questions['medias_terceiro_conteudo'].order_by('?')[:int(len(dictionary_questions['medias_terceiro_conteudo']) * 0.5)]
#                     questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')
#                 if dificuldade_escolhida == 'M':
#                     questoes_terceiro_conteudo = dictionary_questions['terceiro_conteudo'] | dictionary_questions['dificeis_terceiro_conteudo'].order_by('?')[:int(len(dictionary_questions['dificeis_terceiro_conteudo']) * 0.5)] | dictionary_questions['faceis_terceiro_conteudo'].order_by('?')[:int(len(dictionary_questions['faceis_terceiro_conteudo']) * 0.5)]
#                     questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')
#                 if dificuldade_escolhida == 'D':
#                     questoes_terceiro_conteudo = dictionary_questions['terceiro_conteudo'] | dictionary_questions['medias_terceiro_conteudo'].order_by('?')[:int(len(dictionary_questions['medias_terceiro_conteudo']) * 0.5)]
#                     questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')
#                 qtd_conteudos += 1

#             if qtd_conteudos != 0 and questoes_primeiro_conteudo:
#                 if int(quantidade_questoes) % qtd_conteudos == 0:
#                     questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
#                     if questoes_segundo_conteudo:
#                         questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
#                     if questoes_terceiro_conteudo:
#                         questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
#                 else:
#                     questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos + 1]
#                     if questoes_segundo_conteudo:
#                         questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
#                     if questoes_terceiro_conteudo:
#                         questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                
#                 questoes = questoes_primeiro_conteudo
#                 if questoes_segundo_conteudo:
#                     questoes = questoes | questoes_segundo_conteudo
#                 if questoes_terceiro_conteudo:
#                     questoes = questoes | questoes_terceiro_conteudo

#         if dificuldade_escolhida == 'Indefinido' and serie_escolhida != 'Indefinido' or serie_escolhida == 'Indefinido' and dificuldade_escolhida == 'Indefinido':
#             qtd_conteudos = 0
#             if dictionary_questions['primeiro_conteudo']:
#                 questoes_primeiro_conteudo = dictionary_questions['primeiro_conteudo']
#                 qtd_conteudos += 1
#             if dictionary_questions['segundo_conteudo']:
#                 questoes_segundo_conteudo = dictionary_questions['segundo_conteudo']
#                 qtd_conteudos += 1
#             if dictionary_questions['terceiro_conteudo']:
#                 questoes_terceiro_conteudo = dictionary_questions['terceiro_conteudo']
#                 qtd_conteudos += 1

#             if qtd_conteudos != 0 and questoes_primeiro_conteudo:
#                 if int(quantidade_questoes) % qtd_conteudos == 0:
#                     questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
#                     if questoes_segundo_conteudo:
#                         questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
#                     if questoes_terceiro_conteudo:
#                         questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
#                 else:
#                     questoes_primeiro_conteudo = questoes_primeiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos + 1]
#                     if questoes_segundo_conteudo:
#                         questoes_segundo_conteudo = questoes_segundo_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
#                     if questoes_terceiro_conteudo:
#                         questoes_terceiro_conteudo = questoes_terceiro_conteudo.order_by('?')[:int(quantidade_questoes) // qtd_conteudos]
                
#                 questoes = questoes_primeiro_conteudo
#                 if questoes_segundo_conteudo:
#                     questoes = questoes | questoes_segundo_conteudo
#                 if questoes_terceiro_conteudo:
#                     questoes = questoes | questoes_terceiro_conteudo

#         data = self.request.GET.get('data')

#         if data:
#             data = datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')

#         context.update({
#             'questoes': questoes,
#             'nome_disciplina': disciplina_escolhida,
#             'nome_conteudo': conteudo_escolhido,
#             'data': data,
#             'logo': logo,
#             'nome_professor': self.request.GET.get('nome_professor'),
#             'tipo_prova': self.request.GET.get('tipo_prova'),
#             'observacao1': self.request.GET.get('observacao_1'),
#             'observacao2': self.request.GET.get('observacao_2'),
#             'observacao3': self.request.GET.get('observacao_3'),
#             'curso': self.request.GET.get('curso'),
#             'turma': self.request.GET.get('turma'),
#             'bimestre': self.request.GET.get('bimestre')
#         })

#         return context

# class Sobre(ListView):
#     model = Question
#     template_name = 'elaboradorapp/sobre.html'