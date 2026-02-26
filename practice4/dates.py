from datetime import datetime, timedelta

today = datetime.now()
fivedaysago = today - timedelta(days=5)
print(fivedaysago)



today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print(yesterday.date())
print(today.date())
print(tomorrow.date())



now = datetime.now()
cleannow = now.replace(microsecond=0)
print(now)
print(cleannow)


date1 = datetime(2026, 2, 26, 12, 0, 0)
date2 = datetime(2026, 2, 25, 6, 30, 0)
diff = date1 - date2
seconds = diff.total_seconds()
print(seconds)