# Django Celery IP Tracker

This project is a **Django-based IP tracker** with background task processing using **Celery** and **Redis**.  
It demonstrates how to track requests, flag suspicious IP addresses, and schedule background jobs, all orchestrated with **Docker Compose**.

---

## Features

- **Django App** – Main web application with REST APIs and admin panel.
- **Celery Worker** – Processes background tasks (e.g., IP flagging).
- **Celery Beat** – Scheduler for periodic tasks (like a cron service).
- **Redis** – Acts as a broker and result backend for Celery, and as cache for Django.
- **MySQL** – Relational database to store users, requests, and logs.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed  
- [Docker Compose](https://docs.docker.com/compose/) installed

---

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/django-celery-ip-tracker.git
   cd django-celery-ip-tracker
2. Setup .env:

    MYSQL_DATABASE=ip_tracker
    MYSQL_USER=normal_user
    MYSQL_PASSWORD=user
    MYSQL_ROOT_USER=root
    MYSQL_ROOT_PASSWORD=toor