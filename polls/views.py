from django.http import  HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
def newchoice(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
       new_choice=request.POST["new_choice"]
       if not new_choice:
           raise KeyError
    except (KeyError):
        return render(
           request,
           "polls/addchoice.html",
           {
              "question":question,
              "error_message": "choice could not be added",
           },
        
        )
    else:
        newchoice=Choice(
          question=question,
          choice_text=new_choice
     )
        newchoice.save()
        return HttpResponseRedirect(reverse("polls:detail",args=(question.id,)))
    
def vote_reset(request, question_id):
     question = get_object_or_404(Question, pk=question_id)

     for choice in question.choice_set.all():
         choice.votes = 0
         choice.save()

     return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def add_question(request):
     if request.method == 'GET':
         return render(request, "polls/new_question.html", {})
     elif request.method == 'POST':
         user_submitted_question = request.POST["question"]
         if not user_submitted_question:
             return render(request, "polls/new_question.html", {
                 "error_message": "Please enter a valid question"
             })

         new_question = Question(
             question_text=user_submitted_question,
             pub_date=timezone.now(),
         )
         new_question.save()
     return HttpResponseRedirect(reverse("polls:index",))
def update(request,id):
    question = get_object_or_404(Question, id=id)
    if request.method =='GET':
        return render (request,'polls/update_question.html',{'question':question})
    if request.method == "POST":
        newquestion = request.POST.get('input')
        question.question_text = newquestion
        question.save()
        return render (request,'polls/detail.html', {'question': question})
    

def delete(request,id):
    question = get_object_or_404(Question, id=id)
    if request.method =='POST':
        question.delete()
        return redirect('polls:index')
    else:
        return render (request, 'polls/delete_question.html', {'question':question})

