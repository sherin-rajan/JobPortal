from jobs.models import Sectors,Notification

def allSectors(request):
    all_sectors=Sectors.objects.all()
    return dict(sectors=all_sectors)

def notification_count(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return { "notification_count": count}
    return {"notification_count": 0}