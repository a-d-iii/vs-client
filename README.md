# Portal Explorer

Portal Explorer is a lightweight asynchronous Python tool for retrieving
student information from the VTOP portal. It handles session management,
CAPTCHA solving and HTML parsing so you can focus on using the data.

## Features
- Login and maintain a session with VTOP
- Fetch profile, attendance, timetable, exam schedules and marks
- Retrieve biometric logs, outing requests and payment information

## Quick Example
```python
import asyncio
from portal_explorer.session import PortalSession

async def main():
    async with PortalSession("24BES7016", "Vitpassword@1", timeout=60) as session:
        profile = await session.get_profile()
        print(profile)

asyncio.run(main())
```
