class Node {
  idCount = 0;
  constructor(domaine = "") {
    this.id = idCount;
    this.idCount += 1;
    this.domaine = domaine;
  }

  setDomaine(domaine) {
    this.domaine = domaine;
  }
}

class Relation {
  constructor(node1, label, node2) {
    this.node1 = node1;
    this.node2 = node2;
    this.label = label;
  }
}

class Personne extends Node {
  constructor(nom, prenom) {
    super();
    this.nom = nom;
    this.prenom = prenom;
  }
  toString() {
    return `${this.prenom} ${this.nom}`;
  }
}

class Etudiant extends Personne {
  constructor(nom, prenom, promo) {
    super(nom, prenom);
    this.promo = promo;
  }
  toString() {
    return `${super.toString()} (${this.promo})`;
  }
}

class Enseignant extends Personne {
  constructor(nom, prenom, numero) {
    super(nom, prenom);
    this.numero = numero;
  }
  toString() {
    return `${super.toString()} (${this.numero})`;
  }
}

class Promo extends Node {
  constructor(nom) {
    super();
    this.nom = nom;
  }
  toString() {
    return `${this.nom}`;
  }
}

class World {
  constructor() {
    this.nodes = [];
    this.relations = [];
  }
  addNode(node) {
    this.nodes.push(node);
  }
  toString() {
    return this.nodes.map((node) => node.toString()).join("\n");
  }
  linkNodes(node1, relationType, node2) {
    this.relations.push(new Relation(node1, relationType, node2));
  }
}

export { Etudiant, Enseignant, Promo, World };
