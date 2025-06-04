# Variables
VENV_NAME = venv
PYTHON = python3
PIP = $(VENV_NAME)/bin/pip
PYTHON_VENV = $(VENV_NAME)/bin/python
SCRIPTS = automatic_table.py customers_table.py remove_duplicates.py fusion.py

# Couleurs pour les messages
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help setup docker-up docker-down clean run all status

# Aide - affiche les commandes disponibles
help:
	@echo "$(GREEN)Commandes disponibles:$(NC)"
	@echo "  $(YELLOW)make all$(NC)          - Lance tout le processus (setup + docker + run)"
	@echo "  $(YELLOW)make setup$(NC)        - Crée l'environnement virtuel et installe les dépendances"
	@echo "  $(YELLOW)make docker-up$(NC)    - Lance les containers Docker"
	@echo "  $(YELLOW)make run$(NC)          - Exécute tous les scripts dans l'ordre"
	@echo "  $(YELLOW)make status$(NC)       - Affiche le statut des containers"
	@echo "  $(YELLOW)make docker-down$(NC)  - Arrête les containers"
	@echo "  $(YELLOW)make clean$(NC)        - Nettoie tout (containers, volumes, venv)"

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

# Exécute tous les scripts dans l'ordre
run:
	@echo "$(GREEN)Exécution des scripts dans l'ordre...$(NC)"
	@if [ ! -d "$(VENV_NAME)" ]; then \
		echo "$(RED)Erreur: Environnement virtuel non trouvé. Lancez 'make setup' d'abord.$(NC)"; \
		exit 1; \
	fi
	@for script in $(SCRIPTS); do \
		echo "$(YELLOW)Exécution de $script...$(NC)"; \
		if [ ! -f "$script" ]; then \
			echo "$(RED)Erreur: $script non trouvé!$(NC)"; \
			exit 1; \
		fi; \
		$(PYTHON_VENV) $script; \
		if [ $? -ne 0 ]; then \
			echo "$(RED)Erreur lors de l'exécution de $script$(NC)"; \
			exit 1; \
		fi; \
		echo "$(GREEN)$script exécuté avec succès!$(NC)"; \
	done
	@echo "$(GREEN)Tous les scripts ont été exécutés avec succès!$(NC)"

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