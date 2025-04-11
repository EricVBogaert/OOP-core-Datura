#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_document.py - Outil de génération de documents basés sur des concepts

Cet outil permet de créer facilement des documents Python, JSON, Markdown, etc.
en utilisant des templates prédéfinis et en héritant des métadonnées des concepts.
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import jsonschema

# Configuration des chemins
CONCEPT_HOME = os.environ.get('CONCEPT_HOME', os.path.expanduser('~/.concepts'))
TEMPLATES_DIR = os.path.join(CONCEPT_HOME, 'templates')
SCHEMAS_DIR = os.path.join(CONCEPT_HOME, 'schemas')
CONCEPTS_DIR = os.path.join(CONCEPT_HOME, 'concepts')
OUTPUT_DIR = os.getcwd()  # Répertoire courant par défaut


def load_concept(concept_id):
    """Charge un concept depuis la base de connaissances."""
    concept_path = os.path.join(CONCEPTS_DIR, f"{concept_id}.json")
    if not os.path.exists(concept_path):
        print(f"Erreur: Concept '{concept_id}' introuvable.")
        return None

    with open(concept_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_template(template_name, format_type):
    """Charge un template Jinja2."""
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template_path = f"{format_type}/{template_name}.{format_type}.jinja"
    try:
        return env.get_template(template_path)
    except Exception as e:
        print(f"Erreur lors du chargement du template: {e}")
        return None


def validate_metadata(metadata, schema_name):
    """Valide les métadonnées contre un schéma JSON."""
    schema_path = os.path.join(SCHEMAS_DIR, f"{schema_name}.schema.json")
    if not os.path.exists(schema_path):
        print(f"Avertissement: Schéma '{schema_name}' introuvable, validation ignorée.")
        return True

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    try:
        jsonschema.validate(instance=metadata, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Erreur de validation: {e}")
        return False


def merge_with_parent(metadata, parent_concept):
    """Fusionne les métadonnées avec celles du concept parent."""
    if not parent_concept:
        return metadata

    # Copie profonde du concept parent
    merged = json.loads(json.dumps(parent_concept))

    # Liste des champs surchargeables
    overridable = parent_concept.get('structure', {}).get('inheritance', {}).get('overridable', [])

    # Fusionner les champs surchargeables
    for field in overridable:
        if field in metadata:
            if isinstance(metadata[field], dict) and field in merged:
                merged[field].update(metadata[field])
            else:
                merged[field] = metadata[field]

    # Ajouter les champs spécifiques
    for field in metadata:
        if field not in merged:
            merged[field] = metadata[field]

    return merged


def create_document(args):
    """Crée un document basé sur les arguments fournis."""
    # Charger le concept parent si spécifié
    parent_concept = None
    if args.inherits_from:
        parent_concept = load_concept(args.inherits_from)
        if not parent_concept and args.inherits_from != 'none':
            print(f"Avertissement: Concept parent '{args.inherits_from}' introuvable.")

    # Préparer les métadonnées de base
    metadata = {
        "concept_id": args.concept_id,
        "title": args.title,
        "tags": args.tags.split(',') if args.tags else [],
        "context": {
            "primary": args.context
        },
        "expertise": {
            "required": args.expertise_required,
            "target": args.expertise_target
        },
        "domain": {
            "primary": args.domain
        },
        "description": args.description,
        "created_at": datetime.datetime.now().strftime('%Y-%m-%d'),
        "updated_at": datetime.datetime.now().strftime('%Y-%m-%d'),
    }

    # Ajouter des sous-domaines si spécifiés
    if args.subdomains:
        metadata["domain"]["subdomains"] = args.subdomains.split(',')

    # Fusionner avec le concept parent si nécessaire
    if parent_concept:
        metadata["inherits_from"] = args.inherits_from
        metadata = merge_with_parent(metadata, parent_concept)

    # Charger le template
    template = load_template(args.template, args.format)
    if not template:
        return False

    # Valider les métadonnées
    schema_name = f"{args.format}_document"
    if not validate_metadata(metadata, schema_name):
        if not args.force:
            print("Validation échouée. Utilisez --force pour ignorer.")
            return False
        print("Validation échouée, continuation forcée.")

    # Générer le contenu
    try:
        content = template.render(**metadata, now=datetime.datetime.now())
    except Exception as e:
        print(f"Erreur lors de la génération du contenu: {e}")
        return False

    # Créer le fichier de sortie
    output_path = os.path.join(OUTPUT_DIR, args.output)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Document créé avec succès: {output_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier: {e}")
        return False


def list_templates(format_type=None):
    """Liste les templates disponibles."""
    if format_type:
        template_dir = os.path.join(TEMPLATES_DIR, format_type)
        if not os.path.exists(template_dir):
            print(f"Aucun template trouvé pour le format '{format_type}'.")
            return

        templates = [f.split('.')[0] for f in os.listdir(template_dir)
                     if f.endswith(f'.{format_type}.jinja')]
        print(f"Templates disponibles pour '{format_type}':")
        for template in templates:
            print(f"  - {template}")
    else:
        print("Formats disponibles:")
        for d in os.listdir(TEMPLATES_DIR):
            if os.path.isdir(os.path.join(TEMPLATES_DIR, d)):
                print(f"  - {d}")


def main():
    parser = argparse.ArgumentParser(description="Créer un document basé sur un concept")
    parser.add_argument('--concept-id', required=True, help="Identifiant unique du document")
    parser.add_argument('--inherits-from', help="Concept dont ce document hérite (ou 'none')")
    parser.add_argument('--title', required=True, help="Titre du document")
    parser.add_argument('--format', choices=['python', 'json', 'markdown'], required=True,
                        help="Format du document")
    parser.add_argument('--template', required=True, help="Nom du template à utiliser")
    parser.add_argument('--tags', help="Tags séparés par des virgules")
    parser.add_argument('--context', default='enseignement',
                        help="Contexte principal (enseignement, recherche, etc.)")
    parser.add_argument('--expertise-required', default='débutant',
                        help="Niveau d'expertise requis")
    parser.add_argument('--expertise-target', default='débutant',
                        help="Niveau d'expertise ciblé")
    parser.add_argument('--domain', required=True, help="Domaine principal")
    parser.add_argument('--subdomains', help="Sous-domaines séparés par des virgules")
    parser.add_argument('--description', help="Description du document")
    parser.add_argument('--output', required=True, help="Nom du fichier de sortie")
    parser.add_argument('--force', action='store_true', help="Forcer la création même en cas d'erreur de validation")
    parser.add_argument('--list-templates', action='store_true', help="Lister les templates disponibles")
    parser.add_argument('--list-format', help="Lister les templates pour un format spécifique")

    args = parser.parse_args()

    # Créer les répertoires s'ils n'existent pas
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    os.makedirs(SCHEMAS_DIR, exist_ok=True)
    os.makedirs(CONCEPTS_DIR, exist_ok=True)

    # Lister les templates si demandé
    if args.list_templates:
        list_templates()
        return

    if args.list_format:
        list_templates(args.list_format)
        return

    # Créer le document
    create_document(args)


if __name__ == "__main__":
    main()