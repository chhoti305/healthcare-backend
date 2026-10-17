\# Healthcare Backend (Django + DRF + PostgreSQL)



A REST API for managing patients, doctors and patient-doctor assignments, secured with JWT authentication.



\## Tech stack



\- Django, Django REST Framework

\- PostgreSQL

\- JWT auth via djangorestframework-simplejwt



\## Setup



1\. Clone the repo and create a virtual environment:



```

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

```



2\. Create a PostgreSQL database named `healthcare\_db`.

3\. Copy `.env.example` to `.env` and fill in your values.

4\. Run migrations and start the server:



```

python manage.py migrate

python manage.py runserver

```



\## API endpoints



All endpoints except register and login need the header `Authorization: Bearer <access\_token>`.



| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | `/api/auth/register/` | Register (name, email, password) |

| POST | `/api/auth/login/` | Login, returns JWT tokens |

| POST | `/api/patients/` | Add a patient |

| GET | `/api/patients/` | List your patients |

| GET | `/api/patients/{id}/` | Patient details |

| PUT | `/api/patients/{id}/` | Update a patient |

| DELETE | `/api/patients/{id}/` | Delete a patient |

| POST | `/api/doctors/` | Add a doctor |

| GET | `/api/doctors/` | List all doctors |

| GET | `/api/doctors/{id}/` | Doctor details |

| PUT | `/api/doctors/{id}/` | Update a doctor |

| DELETE | `/api/doctors/{id}/` | Delete a doctor |

| POST | `/api/mappings/` | Assign a doctor to a patient |

| GET | `/api/mappings/` | List all mappings |

| GET | `/api/mappings/{patient\_id}/` | Doctors assigned to a patient |

| DELETE | `/api/mappings/{id}/` | Remove a mapping |



\## Notes



\- Patients are visible only to the user who created them.

\- A doctor can be assigned to a patient only once.

\- Secrets are loaded from environment variables (`.env`, not committed).

