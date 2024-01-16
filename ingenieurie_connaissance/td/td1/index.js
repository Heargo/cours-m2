const fs = require("fs");
const { get } = require("http");
const rdf = require("rdflib");

const RDF = rdf.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#");
const RDFS = rdf.Namespace("http://www.w3.org/2000/01/rdf-schema#");
const XSD = rdf.Namespace("http://www.w3.org/2001/XMLSchema#");
const FOAF = rdf.Namespace("http://xmlns.com/foaf/0.1/");
const DC = rdf.Namespace("http://purl.org/dc/elements/1.1/");
const SKOS = rdf.Namespace("http://www.w3.org/2004/02/skos/core#");

const APP = rdf.Namespace("http://hugo.fr/rdf#");

const graph = rdf.graph();

const raw = fs.readFileSync(__dirname + "/example.json").toString();
const data = JSON.parse(raw);

function getId(name) {
  return name.replace(/\s/g, "_");
}

function createObjets() {
  for (let element in data) {
    infos = data[element];
    obj = APP(getId(element));
    graph.add(obj, RDFS("label"), element);
    graph.add(obj, RDF("type"), APP(getId(infos.type)));
    infos.linkedSubjects.forEach((alias) => {
      graph.add(obj, SKOS("altLabel"), getId(alias));
    });
    graph.add(obj, SKOS("definition"), infos.definition);
    graph.add(obj, RDF("pronounce"), infos.pronounce);
    infos.linkedSubjects.forEach((subject) => {
      graph.add(obj, SKOS("related"), APP(getId(subject)));
    });
  }
}

function main() {
  createObjets();
  console.log(graph.toString());
}

main();
