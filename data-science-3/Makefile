# Variables
VENV_NAME = venv
PYTHON = python3
PIP = $(VENV_NAME)/bin/pip

# Couleurs
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m

.PHONY: help setup uninstall run

help:
	@echo "$(GREEN)Commandes disponibles:$(NC)"
	@echo "  $(YELLOW)make setup$(NC)     - Crée le venv et installe les dépendances de requirements.txt"
	@echo "  $(YELLOW)make uninstall$(NC) - Supprime l'environnement virtuel"
	@echo "  $(YELLOW)make run$(NC)       - Lance Jupyter Lab dans le venv"
	@echo "  $(YELLOW)make help$(NC)      - Affiche cette aide"

setup:
	@echo "$(GREEN)Création de l'environnement virtuel et installation des dépendances...$(NC)"
	@if [ ! -d "$(VENV_NAME)" ]; then \
		$(PYTHON) -m virtualenv $(VENV_NAME); \
		echo "$(YELLOW)Environnement virtuel créé$(NC)"; \
	else \
		echo "$(YELLOW)Environnement virtuel déjà existant$(NC)"; \
	fi
	@$(PIP) install --upgrade pip
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "$(RED)Fichier requirements.txt introuvable!$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Installation terminée. Active l'env avec : source $(VENV_NAME)/bin/activate$(NC)"

uninstall:
	@echo "$(YELLOW)Suppression de l'environnement virtuel...$(NC)"
	@if [ -d "$(VENV_NAME)" ]; then \
		rm -rf $(VENV_NAME); \
		echo "$(GREEN)Environnement virtuel supprimé$(NC)"; \
	else \
		echo "$(RED)Aucun environnement virtuel trouvé$(NC)"; \
	fi

run:
	@echo "$(GREEN)Lancement de Jupyter Lab (sans ouvrir le navigateur)...$(NC)"
	@$(VENV_NAME)/bin/jupyter lab --no-browser --ip=127.0.0.1
