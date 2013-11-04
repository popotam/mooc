// Homework 2: Dijkstra's algorithm

#include <iostream>
#include <random>
#include <vector>

using namespace std;

// Constant parameters

const int DEFAULT_GRAPH_SIZE = 50;
const double MIN_COST = 1.0;
const double MAX_COST = 10.0;

// Random Number Generator

random_device r_device{};
default_random_engine r_engine{r_device()};
uniform_real_distribution<> r_cost_distribution(MIN_COST, MAX_COST);
uniform_real_distribution<> r_probability(0.0, 1.0);

double random_cost(void) {
  return r_cost_distribution(r_engine);
}

double random_edge(double density) {
  return r_probability(r_engine) <= density;
}


// Graph related classes

struct Edge {
    double cost;
    long destination;

  public:
    Edge(double cost, long destination):cost(cost),destination(destination){};
    ~Edge(){};

};

ostream& operator<< (ostream& out, Edge edge) {
  return out << "Edge(" << edge.cost << "," << edge.destination << ")";
};


class Vertex {
    vector<Edge> edges;

  public:
    Vertex(){}
    ~Vertex(){}

    long size(void){
      return edges.size();
    }

    void add(Edge edge) {
      edges.push_back(edge);
    }
};

ostream& operator<< (ostream& out, Vertex vertex) {
  return out << "Vertex(" << vertex.size() << ")";
};


class Graph {
    vector<Vertex> vertices;

  public:
    Graph(long size=DEFAULT_GRAPH_SIZE) {
      vertices.resize(size);
    }
    ~Graph(){}

    Vertex get(const long index) {
      return vertices[index];
    }

    long size(void){
      return vertices.size();
    }

    void generate_random_edges(const double density) {
      for (int from = 0; from < size(); ++from) {
        for (int to = from; to < size(); ++to) {
          if (random_edge(density)) {
            double cost = random_cost();
            // add edge from "from" to "to"
            vertices[from].add(Edge(cost, to));
            // add edge the other way - graph is undirected
            vertices[to].add(Edge(cost, from));
          }
        }
      }
    }
};

ostream& operator<< (ostream& out, Graph graph) {
  return out << "Graph(" << graph.size() << ")";
}


class ShortestPath {

};




// ---------- MAIN ----------


int main(void) {
  // prepare a graph with default number of vertices
  Graph graph;
  // generate random edges
  graph.generate_random_edges(0.2);

  cout << graph << endl;
  for(int i = 0; i < DEFAULT_GRAPH_SIZE; ++i)
    cout << graph.get(i) << endl;

  // calculate the sum
  //int accum = sum(data);

  // print the sum to stdout
  //cout << "sum is " << accum << endl;
  return 0;
}
