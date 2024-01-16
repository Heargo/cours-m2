class Node {
  idCount = 0;
  constructor(domaine = "") {
    this.id = this.idCount;
    this.idCount++;
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

  toRdf() {
    let rdf = `<?xml version="1.0"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    xmlns:ld="https://luc-damas.fr/rdg#"
    >\n`;

    // Generate RDF for nodes
    this.nodes.forEach((node) => {
      rdf += `    <rdf:Description rdf:about="${ld}:${node.id}">\n`;
      rdf += `        <foaf:name>${node.nom || node.toString()}</foaf:name>\n`;
      rdf += `        <rdf:type rdf:resource="${ld}:${node.constructor.name}"/>\n`;
      rdf += `    </rdf:Description>\n\n`;
    });

    // Generate RDF for relations
    this.relations.forEach((relation) => {
      rdf += `    <rdf:Description rdf:about="${ld}:${relation.node1.id}">\n`;
      rdf += `        <ld:${relation.label} rdf:resource="${ld}:${relation.node2.id}"/>\n`;
      rdf += `    </rdf:Description>\n\n`;
    });

    rdf += "</rdf:RDF>";
    return rdf;
  }
}

const fs = require("fs");

const raw = fs.readFileSync(__dirname + "\\students.json").toString();
const data = JSON.parse(raw);

world = new World();

for (let element in data) {
  infos = data[element];
  world.addNode(new Etudiant(infos.firstname, infos.lastname, "M2"));
}

console.log(world.nodes);
