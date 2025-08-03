# Variables
VENV_NAME = venv
PYTHON = python3
PIP = $(VENV_NAME)/bin/pip
PYTHON_VENV = $(VENV_NAME)/bin/python
SCRIPT_NAME_0 = automatic_table.py
SCRIPT_NAME_1 = customers_table.py
SCRIPT_NAME_2 = remove_duplicates.py
SCRIPT_NAME_3 = fusion.py

# Couleurs pour les messages
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help setup docker-up docker-down clean run all status logs

# Aide - affiche les commandes disponibles
help:
	@echo "$(GREEN)Commandes disponibles:$(NC)"
	@echo "  $(YELLOW)make all$(NC)          - Lance tout le processus (setup + docker + run)"
	@echo "  $(YELLOW)make setup$(NC)        - Crée l'environnement virtuel et installe les dépendances"
	@echo "  $(YELLOW)make docker-up$(NC)    - Lance les containers Docker"
	@echo "  $(YELLOW)make run$(NC)          - Exécute le script Python"
	@echo "  $(YELLOW)make status$(NC)       - Affiche le statut des containers"
	@echo "  $(YELLOW)make logs$(NC)         - Affiche les logs des containers"
	@echo "  $(YELLOW)make docker-down$(NC)  - Arrête les containers"
	@echo "  $(YELLOW)make clean$(NC)        - Nettoie tout (containers, volumes, venv)"
	@echo "  $(YELLOW)make help$(NC)         - Affiche cette aide"

# Commande principale - lance tout
all: setup docker-up run

# Configuration de l'environnement Python
setup:
	@echo "$(GREEN)Configuration de l'environnement Python...$(NC)"
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "$(YELLOW)Création de l'environnement virtuel...$(NC)"; \
		$(PYTHON) -m venv $(VENV_NAME); \
	fi
	@echo "$(YELLOW)Installation des dépendances...$(NC)"
	@$(PIP) install --upgrade pip
	@if [ -f "requirements.txt" ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "$(RED)Attention: requirements.txt non trouvé$(NC)"; \
	fi
	@echo "$(GREEN)Environnement Python configuré!$(NC)"

# Lance Docker Compose
docker-up:
	@echo "$(GREEN)Lancement des containers Docker...$(NC)"
	@docker compose up -d --build
	@echo "$(YELLOW)Attente du démarrage de PostgreSQL...$(NC)"
	@sleep 10
	@echo "$(GREEN)Containers Docker lancés!$(NC)"
	@make status

# Affiche le statut des containers
status:
	@echo "$(GREEN)Statut des containers:$(NC)"
	@docker compose ps

# Affiche les logs
logs:
	@echo "$(GREEN)Logs des containers:$(NC)"
	@docker compose logs

# Exécute les scripts Python
run:
	@echo "$(GREEN)Exécution des scripts Python...$(NC)"
	@if [ ! -f "$(SCRIPT_NAME_0)" ]; then \
		echo "$(RED)Erreur: $(SCRIPT_NAME_0) non trouvé!$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "$(SCRIPT_NAME_1)" ]; then \
		echo "$(RED)Erreur: $(SCRIPT_NAME_1) non trouvé!$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "$(SCRIPT_NAME_2)" ]; then \
		echo "$(RED)Erreur: $(SCRIPT_NAME_2) non trouvé!$(NC)"; \
		exit 1; \
	fi
	@if [ ! -f "$(SCRIPT_NAME_3)" ]; then \
		echo "$(RED)Erreur: $(SCRIPT_NAME_3) non trouvé!$(NC)"; \
		exit 1; \
	fi
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "$(RED)Erreur: Environnement virtuel non trouvé. Lancez 'make setup' d'abord.$(NC)"; \
		exit 1; \
	fi
	@$(PYTHON_VENV) $(SCRIPT_NAME_0)
	@$(PYTHON_VENV) $(SCRIPT_NAME_1)
	@$(PYTHON_VENV) $(SCRIPT_NAME_2)
	@$(PYTHON_VENV) $(SCRIPT_NAME_3)
	@echo "$(GREEN)Scripts exécutés avec succès!$(NC)"

# Arrête les containers
docker-down:
	@echo "$(YELLOW)Arrêt des containers Docker...$(NC)"
	@docker compose down

# Nettoie tout
clean:
	@echo "$(YELLOW)Nettoyage en cours...$(NC)"
	@docker compose down -v
	@docker system prune -a --volumes -f
	@if [ -d "$(VENV_NAME)" ]; then \
		echo "$(YELLOW)Suppression de l'environnement virtuel...$(NC)"; \
		rm -rf $(VENV_NAME); \
	fi
	@echo "$(GREEN)Nettoyage terminé!$(NC)"

# Redémarre tout
restart: docker-down docker-up

# Commande pour se connecter à PostgreSQL
db-connect:
	@echo "$(GREEN)Connexion à PostgreSQL...$(NC)"
	@docker exec -it postgres_local psql -U smonte -d piscineds

# Commande pour ouvrir pgAdmin
pgadmin:
	@echo "$(GREEN)pgAdmin disponible sur: http://localhost:8080$(NC)"
	@echo "$(YELLOW)Email: admin@admin.com$(NC)"
	@echo "$(YELLOW)Password: admin$(NC)"