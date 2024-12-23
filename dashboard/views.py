from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('dashboard:user_dashboard')
    return render(request, 'dashboard/admin_dashboard.html')
