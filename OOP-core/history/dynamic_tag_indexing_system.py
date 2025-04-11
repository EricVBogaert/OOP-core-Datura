#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
concept_id: tag-index-manage-2025
inherits_from: OOP-core-concept-2025
title: Système d'indexation dynamique des tags
version: 1.0.0

tags:
    - python          # langage de programmation
    - indexation      # action principale
    - tags            # objet manipulé
    - graphe          # structure de données
    - hiérarchie      # type de relation
    - dynamique       # caractéristique du système

context:
    primary: développement
    secondary: recherche

expertise:
    required: intermédiaire
    target: avancé

domain:
    primary: informatique
    subdomains:
        - programmation
        - gestion_connaissances
        - recherche_information

application:
    type: bibliothèque
    input: tags_et_relations
    output: index_recherchable

dependencies:
    - python>=3.8
    - networkx>=2.6
    - sqlite3

authors:
    - name: UCLouvain Knowledge Systems Team

created_at: 2025-04-10
updated_at: 2025-04-10

Ce module implémente un système d'indexation dynamique des tags avec gestion
des relations hiérarchiques (ascendantes/descendantes) et contextuelles.
Il permet d'indexer, de rechercher et de visualiser les relations entre tags
dans un système de gestion des connaissances basé sur les concepts.
"""
""""""
Introduction:
Application pratique : Système d'indexation dynamique des tags
Pour implémenter le système d'indexation dynamique des tags avec leurs références ascendantes et descendantes, voici comment nous pourrions concevoir un module Python :
""""""
""""""
Conclusion:
[break]
""""""


import os
import json
import sqlite3
import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Union, Any
import networkx as nx
from collections import defaultdict


class TagRelationship:
    """Types de relations entre tags."""
    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"
    RELATED_TO = "related_to"
    PREREQUISITE_FOR = "prerequisite_for"
    REQUIRES = "requires"
    EQUIVALENT_TO = "equivalent_to"


class TagIndex:
    """
    Système d'indexation dynamique des tags avec gestion des relations
    hiérarchiques et contextuelles.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialise l'index de tags.

        Args:
            db_path: Chemin vers la base de données SQLite (None pour mémoire)
        """
        self.db_path = db_path or ":memory:"
        self.conn = self._init_database()
        self.graph = nx.DiGraph()
        self._load_graph_from_db()

    def _init_database(self) -> sqlite3.Connection:
        """Initialise la base de données SQLite."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table des tags
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        ''')

        # Table des relations entre tags
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tag_relations (
            source_id TEXT,
            target_id TEXT,
            relationship TEXT NOT NULL,
            strength REAL DEFAULT 1.0,
            created_at TEXT,
            updated_at TEXT,
            PRIMARY KEY (source_id, target_id, relationship),
            FOREIGN KEY (source_id) REFERENCES tags (id),
            FOREIGN KEY (target_id) REFERENCES tags (id)
        )
        ''')

        # Table des documents liés aux tags
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_tags (
            document_id TEXT,
            tag_id TEXT,
            weight REAL DEFAULT 1.0,
            created_at TEXT,
            FOREIGN KEY (tag_id) REFERENCES tags (id),
            PRIMARY KEY (document_id, tag_id)
        )
        ''')

        # Créer des index pour optimiser les recherches
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tag_relations_source ON tag_relations (source_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tag_relations_target ON tag_relations (target_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_document_tags_tag ON document_tags (tag_id)')

        conn.commit()
        return conn

    def _load_graph_from_db(self):
        """Charge le graphe de tags depuis la base de données."""
        cursor = self.conn.cursor()

        # Charger les tags comme nœuds
        cursor.execute('SELECT id, name, type, description FROM tags')
        for row in cursor.fetchall():
            tag_id, name, tag_type, description = row
            self.graph.add_node(tag_id, name=name, type=tag_type, description=description)

        # Charger les relations comme arêtes
        cursor.execute('SELECT source_id, target_id, relationship, strength FROM tag_relations')
        for row in cursor.fetchall():
            source_id, target_id, relationship, strength = row
            self.graph.add_edge(source_id, target_id,
                                relationship=relationship,
                                strength=float(strength))

    def add_tag(self, tag_id: str, name: str, tag_type: str,
                description: Optional[str] = None) -> bool:
        """
        Ajoute un nouveau tag à l'index.

        Args:
            tag_id: Identifiant unique du tag
            name: Nom lisible du tag
            tag_type: Type de tag (domain, concept, technology...)
            description: Description optionnelle du tag

        Returns:
            True si ajouté avec succès, False sinon
        """
        try:
            cursor = self.conn.cursor()
            now = datetime.datetime.now().isoformat()

            cursor.execute(
                'INSERT INTO tags (id, name, type, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
                (tag_id, name, tag_type, description, now, now)
            )
            self.conn.commit()

            # Ajouter au graphe
            self.graph.add_node(tag_id, name=name, type=tag_type, description=description)
            return True
        except sqlite3.IntegrityError:
            # Tag déjà existant
            return False

    def add_relationship(self, source_id: str, target_id: str,
                         relationship: str, strength: float = 1.0) -> bool:
        """
        Ajoute une relation entre deux tags.

        Args:
            source_id: ID du tag source
            target_id: ID du tag cible
            relationship: Type de relation (parent_of, related_to, etc.)
            strength: Force de la relation (0.0 à 1.0)

        Returns:
            True si ajouté avec succès, False sinon
        """
        try:
            cursor = self.conn.cursor()
            now = datetime.datetime.now().isoformat()

            # Vérifier que les deux tags existent
            cursor.execute('SELECT id FROM tags WHERE id IN (?, ?)', (source_id, target_id))
            if len(cursor.fetchall()) != 2:
                return False

            cursor.execute(
                '''INSERT OR REPLACE INTO tag_relations 
                   (source_id, target_id, relationship, strength, created_at, updated_at) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (source_id, target_id, relationship, strength, now, now)
            )
            self.conn.commit()

            # Ajouter au graphe
            self.graph.add_edge(source_id, target_id,
                                relationship=relationship,
                                strength=strength)

            # Ajouter la relation inverse si nécessaire
            if relationship == TagRelationship.PARENT_OF:
                self.add_relationship(target_id, source_id, TagRelationship.CHILD_OF, strength)
            elif relationship == TagRelationship.CHILD_OF:
                self.add_relationship(target_id, source_id, TagRelationship.PARENT_OF, strength)
            elif relationship == TagRelationship.PREREQUISITE_FOR:
                self.add_relationship(target_id, source_id, TagRelationship.REQUIRES, strength)
            elif relationship == TagRelationship.REQUIRES:
                self.add_relationship(target_id, source_id, TagRelationship.PREREQUISITE_FOR, strength)
            elif relationship == TagRelationship.RELATED_TO:
                # Relation symétrique, vérifier qu'elle n'existe pas déjà dans l'autre sens
                cursor.execute(
                    'SELECT 1 FROM tag_relations WHERE source_id = ? AND target_id = ? AND relationship = ?',
                    (target_id, source_id, relationship)
                )
                if not cursor.fetchone():
                    self.add_relationship(target_id, source_id, relationship, strength)

            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de la relation: {e}")
            return False

    def tag_document(self, document_id: str, tag_id: str, weight: float = 1.0) -> bool:
        """
        Associe un tag à un document.

        Args:
            document_id: ID du document
            tag_id: ID du tag
            weight: Poids du tag pour ce document (0.0 à 1.0)

        Returns:
            True si ajouté avec succès, False sinon
        """
        try:
            cursor = self.conn.cursor()
            now = datetime.datetime.now().isoformat()

            # Vérifier que le tag existe
            cursor.execute('SELECT id FROM tags WHERE id = ?', (tag_id,))
            if not cursor.fetchone():
                return False

            cursor.execute(
                '''INSERT OR REPLACE INTO document_tags 
                   (document_id, tag_id, weight, created_at) 
                   VALUES (?, ?, ?, ?)''',
                (document_id, tag_id, weight, now)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors du taggage du document: {e}")
            return False

    def get_tag_ancestors(self, tag_id: str,
                          max_depth: int = -1) -> List[Dict[str, Any]]:
        """
        Récupère tous les ancêtres d'un tag (hiérarchie ascendante).

        Args:
            tag_id: ID du tag
            max_depth: Profondeur maximale (-1 pour illimité)

        Returns:
            Liste des tags ancêtres avec leurs métadonnées
        """
        ancestors = []
        visited = set()

        def dfs(current_id, depth=0):
            if current_id in visited or (max_depth >= 0 and depth > max_depth):
                return

            visited.add(current_id)

            # Récupérer les parents directs
            for parent, child, data in self.graph.in_edges(current_id, data=True):
                if data.get('relationship') == TagRelationship.PARENT_OF:
                    if parent not in visited:
                        node_data = self.graph.nodes[parent]
                        ancestors.append({
                            'id': parent,
                            'name': node_data.get('name', parent),
                            'type': node_data.get('type', 'unknown'),
                            'description': node_data.get('description', ''),
                            'distance': depth + 1
                        })
                        dfs(parent, depth + 1)

        dfs(tag_id)
        return ancestors

    def get_tag_descendants(self, tag_id: str,
                            max_depth: int = -1) -> List[Dict[str, Any]]:
        """
        Récupère tous les descendants d'un tag (hiérarchie descendante).

        Args:
            tag_id: ID du tag
            max_depth: Profondeur maximale (-1 pour illimité)

        Returns:
            Liste des tags descendants avec leurs métadonnées
        """
        descendants = []
        visited = set()

        def dfs(current_id, depth=0):
            if current_id in visited or (max_depth >= 0 and depth > max_depth):
                return

            visited.add(current_id)

            # Récupérer les enfants directs
            for parent, child, data in self.graph.out_edges(current_id, data=True):
                if data.get('relationship') == TagRelationship.PARENT_OF:
                    if child not in visited:
                        node_data = self.graph.nodes[child]
                        descendants.append({
                            'id': child,
                            'name': node_data.get('name', child),
                            'type': node_data.get('type', 'unknown'),
                            'description': node_data.get('description', ''),
                            'distance': depth + 1
                        })
                        dfs(child, depth + 1)

        dfs(tag_id)
        return descendants

    def get_related_tags(self, tag_id: str,
                         relationship: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Récupère tous les tags liés à un tag donné.

        Args:
            tag_id: ID du tag
            relationship: Type de relation spécifique (None pour toutes)

        Returns:
            Liste des tags liés avec leurs métadonnées et type de relation
        """
        related = []

        # Récupérer les liens sortants
        for _, target, data in self.graph.out_edges(tag_id, data=True):
            edge_relationship = data.get('relationship')
            if relationship is None or edge_relationship == relationship:
                node_data = self.graph.nodes[target]
                related.append({
                    'id': target,
                    'name': node_data.get('name', target),
                    'type': node_data.get('type', 'unknown'),
                    'description': node_data.get('description', ''),
                    'relationship': edge_relationship,
                    'direction': 'outgoing',
                    'strength': data.get('strength', 1.0)
                })

        # Récupérer les liens entrants
        for source, _, data in self.graph.in_edges(tag_id, data=True):
            edge_relationship = data.get('relationship')
            if relationship is None or edge_relationship == relationship:
                node_data = self.graph.nodes[source]
                # Éviter les doublons pour les relations symétriques
                if edge_relationship != TagRelationship.RELATED_TO or not any(r['id'] == source for r in related):
                    related.append({
                        'id': source,
                        'name': node_data.get('name', source),
                        'type': node_data.get('type', 'unknown'),
                        'description': node_data.get('description', ''),
                        'relationship': edge_relationship,
                        'direction': 'incoming',
                        'strength': data.get('strength', 1.0)
                    })

        return related

    def search_tags(self, query: str,
                    tag_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Recherche des tags par nom ou description.

        Args:
            query: Texte à rechercher
            tag_types: Types de tags à inclure (None pour tous)

        Returns:
            Liste des tags correspondants
        """
        cursor = self.conn.cursor()

        if tag_types:
            placeholders = ', '.join(['?' for _ in tag_types])
            cursor.execute(
                f'''SELECT id, name, type, description 
                   FROM tags 
                   WHERE (name LIKE ? OR description LIKE ?) 
                   AND type IN ({placeholders})
                   ORDER BY name''',
                (f'%{query}%', f'%{query}%', *tag_types)
            )
        else:
            cursor.execute(
                '''SELECT id, name, type, description 
                   FROM tags 
                   WHERE name LIKE ? OR description LIKE ?
                   ORDER BY name''',
                (f'%{query}%', f'%{query}%')
            )

        results = []
        for row in cursor.fetchall():
            tag_id, name, tag_type, description = row
            results.append({
                'id': tag_id,
                'name': name,
                'type': tag_type,
                'description': description
            })

        return results

    def get_documents_by_tag(self, tag_id: str,
                             include_descendants: bool = False) -> List[str]:
        """
        Récupère tous les documents associés à un tag.

        Args:
            tag_id: ID du tag
            include_descendants: Si True, inclut les documents tagués avec des descendants

        Returns:
            Liste des IDs de documents
        """
        cursor = self.conn.cursor()

        if not include_descendants:
            cursor.execute(
                'SELECT document_id FROM document_tags WHERE tag_id = ?',
                (tag_id,)
            )
            return [row