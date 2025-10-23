from .models import CommunityLeader

def leader_flags(request):
    if not request.user.is_authenticated:
        return {}
    is_leader = CommunityLeader.objects.filter(user=request.user).exists()
    return {"is_leader": is_leader}
