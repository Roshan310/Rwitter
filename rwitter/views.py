from django.shortcuts import redirect, render

from rwitter.forms import RweetForm

from .models import Profile, Rweets

# Create your views here.
def dashboard(request):
    form = RweetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            rweet = form.save(commit=False)
            rweet.user = request.user
            rweet.save()
            return redirect('dashboard')

    followed_rweets = Rweets.objects.filter(
        user__profile__in = request.user.profile.follows.all()

    ).order_by('-created_at')

    context = {'form': form, 'rweets': followed_rweets}
    return render(request, 'dashboard.html', context)


def profile_list(request):
    profiles = Profile.objects.exclude(user = request.user)
    context = {'profiles': profiles}
    return render(request, 'profile_list.html', context)

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_user_profile = Profile(user = request.user)
        missing_user_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get('follow')
        if action == 'follow':
            current_user_profile.follows.add(profile)
        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, 'profile.html', {'profile': profile})