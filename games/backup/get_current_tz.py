import datetime

now = datetime.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
print(local_tz)
local_tzname = local_tz.tzname(local_now)
print(local_tzname)
