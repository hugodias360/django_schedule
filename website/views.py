from django.core.serializers import json
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext, context
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, FormView
from .models import cliente, cabeleleiro, servico, agendamento, produto
from decimal import Decimal
from datetime import date, datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import ContactForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model



User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
                    "form": form
              }
    if form.is_valid():
        print(form.cleaned_data)
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
        return render(request, 'registration/login.html', context)
    else:
        return render(request, "registration/register.html", context)



## clientes
@login_required
def indexCliente(request):
    clientes = cliente.objects.all()
    context = {'clientes' : clientes}
    return render(request, 'website/cliente/index.html',context)

@login_required
def createCliente(request):
    clientes = cliente()
    if request.method == 'POST':
        clientes.apelido= request.POST['apelido']
        clientes.senha = request.POST['senha']
        clientes.nome = request.POST['nome']
        clientes.email = request.POST['email']
        clientes.celular =  request.POST['celular']
        clientes.save()
        return HttpResponseRedirect('/cliente')
    else:
        return render(request, 'website/cliente/create.html')

def editCliente(request, id):
    clientes = cliente.objects.get(id=id)
    context = {'clientes': clientes}
    return render(request, 'website/cliente/edit.html', context)

def updateCliente(request, id):
    clientes = cliente.objects.get(id=id)

    clientes.nome = request.POST['nome']
    clientes.email = request.POST['email']
    clientes.celular = request.POST['celular']
    clientes.senha = request.POST['senha']
    clientes.apelido = request.POST['apelido']
    clientes.save()
    return redirect('/cliente')

def deleteCliente(request, id):
    clientes = cliente.objects.get(id=id)
    clientes.delete()
    return redirect('/cliente')

## cabeleleiros

def indexCabeleleiro(request):
    cabeleleiros = cabeleleiro.objects.all()
    context = {'cabeleleiros' : cabeleleiros}
    return render(request, 'website/cabeleleiro/index.html',context)

def createCabeleleiro(request):
    cabeleleiros = cabeleleiro()
    if request.method == 'POST':
        cabeleleiros.senha = request.POST['senha']
        cabeleleiros.nome = request.POST['nome']
        cabeleleiros.email = request.POST['email']
        cabeleleiros.celular =  request.POST['celular']
        cabeleleiros.save()
        return HttpResponseRedirect('/cabeleleiro')
    else:
        return render(request, 'website/cabeleleiro/create.html')

def editCabeleleiro(request, id):
    cabeleleiros = cabeleleiro.objects.get(id=id)
    context = {'cabeleleiros': cabeleleiros}
    return render(request, 'website/cabeleleiro/edit.html', context)

def updateCabeleleiro(request, id):
    cabeleleiros = cabeleleiro.objects.get(id=id)

    cabeleleiros.nome = request.POST['nome']
    cabeleleiros.email = request.POST['email']
    cabeleleiros.celular = request.POST['celular']
    cabeleleiros.senha = request.POST['senha']
    cabeleleiros.save()
    return redirect('/cabeleleiro')

def deleteCabeleleiro(request, id):
    cabeleleiross = cabeleleiro.objects.get(id=id)
    cabeleleiross.delete()
    return redirect('/cabeleleiro')


## Produtos

def editProduto(request, id):
    produtos = produto.objects.get(id=id)
    context = {'produtos': produtos}
    return render(request, 'website/produto/edit.html', context)

def updateProduto(request, id):
    produtos = produto.objects.get(id=id)

    produtos.nome = request.POST['nome']
    valor = request.POST['valor']
    produtos.valor_unitario= Decimal(valor.replace(',', '.'))
    produtos.quantidade = request.POST['quant']
    produtos.save()
    messages.info(request, 'Alterações salvas com sucesso');
    return redirect('/produto')

def deleteProduto(request, pk):
    produtos = produto.objects.get(id=pk)
    produtos.delete()
    messages.info(request, 'Produto excluído');
    return HttpResponseRedirect(reverse_lazy('website:indexProduto'))

## Servicos

def indexServico(request):
    servicos = servico.objects.all()
    context = {'servicos' : servicos}
    return render(request, 'website/servico/index.html',context)

def createServico(request):
    servicos = servico()
    if request.method == 'POST':
        servicos.nome= request.POST['nome']
        valor = request.POST['valor']
        servicos.valor = Decimal(valor.replace(',',''))
        servicos.save()
        return HttpResponseRedirect('/servico')
    else:
        return render(request, 'website/servico/create.html')

def editServico(request, id):
    servicos = servico.objects.get(id=id)
    context = {'servicos': servicos}
    return render(request, 'website/servico/edit.html', context)

def updateServico(request, id):
    servicos = servico.objects.get(id=id)

    servicos.nome = request.POST['nome']
    valor = request.POST['valor']
    servicos.valor = Decimal(valor.replace(',', '.'))
    servicos.save()
    return redirect('/servico')

def deleteServico(request, id):
    servicos = servico.objects.get(id=id)
    servicos.delete()
    return redirect('/servico')

#agendamento
def indexAgendamento(request):
    agendamentos = agendamento.objects.all()
    context = {'agendamentos' : agendamentos}
    return render(request, 'website/agenda/index.html',context)

def createAgendamento(request):
    agendamentos = agendamento()
    if request.method == 'POST':
        servicos = servico.objects.get(id=int(request.POST['servico']))
        clientes = cliente.objects.get(id=int(request.POST['cliente']))
        cabeleleiros = cabeleleiro.objects.get(id=int(request.POST['cabeleleiro']))
        agendamentos.data_inicio= request.POST['data_inicio']
        agendamentos.data_fim = request.POST['data_fim']
        agendamentos.clientes =  clientes
        agendamentos.cabeleleiros = cabeleleiros
        agendamentos.servicos = servicos
        agendamentos.save()
        return HttpResponseRedirect('/agenda')
    else:
        clientes = cliente.objects.all()
        servicos = servico.objects.all()
        cabeleleiros = cabeleleiro.objects.all()

        context = {'clientes' : clientes,'servicos' : servicos,'cabeleleiros' : cabeleleiros}
        return render(request, 'website/agenda/create.html',context)

def editAgendamento(request, id):
    agendamentos = agendamento.objects.get(id=id)
    clientes = cliente.objects.all()
    servicos = servico.objects.all()
    cabeleleiros = cabeleleiro.objects.all()
    agendamentos.data_inicio = agendamentos.data_inicio
    context = {'agendamentos': agendamentos, 'clientes' : clientes,'servicos' : servicos,'cabeleleiros' : cabeleleiros}
    return render(request, 'website/agenda/edit.html', context)

def updateAgendamento(request, id):
    agendamentos = agendamento.objects.get(id=id)
    servicos = servico.objects.get(id=int(request.POST['servico']))
    clientes = cliente.objects.get(id=int(request.POST['cliente']))
    cabeleleiros = cabeleleiro.objects.get(id=int(request.POST['cabeleleiro']))
    agendamentos.data_inicio= request.POST['data']
    agendamentos.clientes = clientes
    agendamentos.cabeleleiros = cabeleleiros
    agendamentos.servicos = servicos
    agendamentos.save()

    return redirect('/agenda')

def deleteAgendamento(request, id):
    agendamentos = agendamento.objects.get(id=id)
    agendamentos.delete()
    return redirect('/agenda')

def testAgendamento(request):
    all_events = agendamento.objects.all()
    #get_event_types = Events.objects.only('event_type')

    if request.GET:
        event_arr = []
        if request.GET.get('event_type') == "all":
            all_events = agendamento.objects.all()
     #   else:
     #       all_events = agendamento.objects.filter(event_type__icontains=request.GET.get('event_type'))

        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.event_name
            start_date = datetime.datetime.strptime(str(i.DATA.date()), "%Y-%m-%d %H:%M:%S'").strftime("%Y-%m-%d %H:%M:%S'")
            end_date = datetime.datetime.strptime(str(i.DATA.date()), "%Y-%m-%d %H:%M:%S'").strftime("%Y-%m-%d %H:%M:%S'")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

    context = {"events":all_events}
    return render(request, 'website/agenda/calendar.html',context)


class CreateUserForm(FormView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('website:login')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'website/calendar.html'

class HomeView(TemplateView):
    template_name = 'website/home.html'

class ProdutoCreateView(CreateView):
    model = produto
    template_name = 'website/produto/create.html'
    fields = ['nome', 'quantidade', 'validade_produto', 'valor_unitario', 'especificacao']
    success_url = reverse_lazy('website:indexProduto')

class ProdutoListView(ListView):
    model = produto
    template_name = 'website/produto/index.html'




def get_data(request):
    data = [
        dict(title='Lunch', start='2018-10-22 10:00', end='2018-10-22 10:30', allDay=False, className='event-azure'),
        dict(title='Lunch', start='2018-10-23 11:00', end='2018-10-22 11:30', allDay=False, className='event-orange'),
        dict(title='Lunch', start='2018-10-24 12:00', end='2018-10-22 12:30', allDay=False, className='event-green'),
        dict(title='Lunch', start='2018-10-25 13:00', end='2018-10-22 13:30', allDay=False, className='event-red'),
        dict(title='Lunch', start='2018-10-26 14:00', end='2018-10-22 14:30', allDay=False, className='event-blue')
    ]
    return JsonResponse(data, safe=False)
