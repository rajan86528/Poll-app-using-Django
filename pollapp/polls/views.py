from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import Choice, Poll
from django.shortcuts import redirect, render
from django.views import View

from .forms import PollForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout

from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:list')
    else:
        form = RegistrationForm()
    return render(request, 'polls/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:list')
        else:
            return render(request, 'polls/login.html', {'error_message': 'Invalid login credentials.'})
    else:
        return render(request, 'polls/login.html')




def user_logout(request):
    logout(request)
    return redirect('polls:index')



class PollListView(View):
    def get(self, request):
        polls = Poll.objects.all()
        return render(request, 'polls/poll_list.html', {'polls': polls})


class PollDetailView(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        choices = poll.choice_set.all()
        voted_choice = request.session.get(f'voted_choice_{poll_id}')
        return render(request, 'polls/poll_detail.html', {'poll': poll, 'choices': choices, 'voted_choice': voted_choice})

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        choice_id = request.POST.get('choice')
        if not choice_id:
            return render(request, 'polls/poll_detail.html', {
                'poll': poll,
                'choices': poll.choice_set.all(),
                'error_message': "Please select a valid choice.",
            })
        choice = get_object_or_404(Choice, pk=choice_id)
        voted_choice = request.session.get(f'voted_choice_{poll_id}')
        if voted_choice:
            return redirect('polls:results', poll_id=poll_id)
        choice.votes += 1
        choice.save()
        request.session[f'voted_choice_{poll_id}'] = choice_id
        return redirect('polls:results', poll_id=poll_id)


class PollResultsView(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        return render(request, 'polls/poll_results.html', {'poll': poll})


# @login_required(login_url='polls:login')
class CreatePollView(View):
    def get(self, request):
        form = PollForm()
        return render(request, 'polls/create_poll.html', {'form': form})

    def post(self, request):
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save()
            choice_texts = request.POST.getlist('choice_texts[]')
            for choice_text in choice_texts:
                if choice_text:
                    Choice.objects.create(poll=poll, choice_text=choice_text)
            return redirect('polls:detail', poll_id=poll.id)
        return render(request, 'polls/create_poll.html', {'form': form})


