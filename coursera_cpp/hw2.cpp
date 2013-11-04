// Homework 2: Dijkstra's algorithm
//
// This script is used to perform two experiments
// on undirected random graphs.
// Average shortest paths are calculated
// for two 50-node graphs with edge density = 0.2 and 0.4

#include <iostream>
#include <limits>
#include <queue>
#include <random>
#include <tuple>
#include <vector>

using namespace std;

// -------------------
// Constant parameters
// -------------------

const int DEFAULT_GRAPH_SIZE = 50;
const double MIN_COST = 1.0;
const double MAX_COST = 10.0;
const double INF = numeric_limits<double>::infinity();


// --------------------------------
// Prepare random number generators
// --------------------------------

random_device r_device{};
default_random_engine r_engine{r_device()};
uniform_real_distribution<> r_cost_distribution(MIN_COST, MAX_COST);
uniform_real_distribution<> r_probability(0.0, 1.0);

// Returns random cost
double random_cost(void) {
  return r_cost_distribution(r_engine);
}

// Returns true if an edge is selected
double random_edge(double density) {
  return r_probability(r_engine) <= density;
}


// ---------------------
// Graph related classes
// ---------------------

// Class for single edge containing edge cost and destination
// Edge in this setup is directed, so for an undirected graph
// a corresponding edge must exist on the destination vertex
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


// Class for single vertex containing a list of edges
class Vertex {
    long id;  // set later by the Graph constructor
    vector<Edge> edges;  // container for vertex neighbors

  public:
    // public data members used as helpers by pathfinding algorithm
    double cost_marker;  // stores vertex cost on currently calculated path
    bool on_closed_list;  // marks if vertex was visited on current run
    long parent;  // id of vertex that leads to this on the shortest path

    Vertex() {
      clear();
    }
    ~Vertex() {}

    long get_id(void) {
      return id;
    }

    void set_id(long new_id) {
      id = new_id;
    }

    long size(void) {
      return edges.size();
    }

    void add(Edge edge) {
      edges.push_back(edge);
    }

    // Clears Vertex's helper data members
    void clear(void) {
      cost_marker = INF;
      on_closed_list = false;
      parent = -1;
    }

    vector<Edge> neighbors(void) {
      return edges;
    }

};

ostream& operator<< (ostream& out, Vertex vertex) {
  return out << "Vertex(" << vertex.size() << ")";
};


// Comparator struct used as a helper in priority_queue in find_path
// It is used to sort vertices with lowest cost to the top of the queue
struct OrderByCostMarker
{
    bool operator() (Vertex const &a, Vertex const &b) {
      return a.cost_marker > b.cost_marker;
    }
};


// Class respresenting random graph
class Graph {
    vector<Vertex> vertices;

  public:
    Graph(long size=DEFAULT_GRAPH_SIZE) {
      cout << "Creating graph with " << size << " vertices" << endl;
      vertices.resize(size);
      // update vertex id for newly created vertices
      for (int i = 0; i < size; ++i) {
        vertices[i].set_id(i);
      }
    }
    ~Graph(){}

    Vertex& get(const long index) {
      return vertices[index];
    }

    long size(void) {
      return vertices.size();
    }

    // Calculates number of egdes by iterating through all of graph's vertices
    long num_edges(void) {
      long sum = 0;
      for (auto vertex : vertices) {
        sum += vertex.size();
      }
      return sum / 2;  // graph is undirected, so we divide by 2
    }

    // Clears Vertex's helper data members
    void clear(void) {
      for (auto vertex : vertices) {
        vertex.clear();
      }
    }

    // Generates random edges with given probability (density param)
    // Graph is undirected, so the method only visits unique pairs
    // of vertices to determine if the edge should be created,
    // and if so it creates an edge in two ways.
    void generate_random_edges(const double density) {
      cout << "Generating edges for graph with density=" << density << endl;
      for (int src = 0; src < size() - 1; ++src) {
        for (int dst = src + 1; dst < size(); ++dst) {
          if (random_edge(density)) {
            double cost = random_cost();
            // add edge from src to dst
            vertices[src].add(Edge(cost, dst));
            // add edge from dst to src - graph is undirected
            vertices[dst].add(Edge(cost, src));
          }
        }
      }
      cout << "Generated " << num_edges() << " edges" << endl;
    }
};

ostream& operator<< (ostream& out, Graph graph) {
  return out << "Graph(vertices=" << graph.size()
    << ", edges=" << graph.num_edges() << ")";
}


// Class responsible for creating a random graph with given size and density
// and calculating average shortest paths.
class ShortestPathExperiment {
    Graph graph;

  public:
    ShortestPathExperiment(const long size, const double density):graph(size) {
      graph.generate_random_edges(density);
    }
    ~ShortestPathExperiment(){}

    double calculate_avg_path_cost(void) {
      int succesful_paths = 0;
      double cost = 0.0;
      double subcost;
      for (int i = 0; i < graph.size() - 1; ++i) {
        // try to calculate path cost for each consecutibe pair of vertices
        try {
          cout << "Calculating path from " << i << " to " << i + 1 << endl;
          subcost = path_cost(i, i + 1);
          cout << "Cost = " << subcost << endl;
          cost += subcost;
          succesful_paths++;
        } catch (exception& e) {
          cout << "Could not find a path from " << i << " to " << i + 1 << endl;
        }
      }
      if (succesful_paths > 0) {
        // take the average
        cost /= succesful_paths;
      }
      return cost;
    }

    // Returns a tuple containing shortest path and it's cost
    tuple<vector<long>, double> find_path(long src, long dst) {
      // prepare a priority queue for the algorithm
      priority_queue<Vertex, vector<Vertex>, OrderByCostMarker> open_queue;
      bool success = false;
      // clear graph of pathfinding markers
      graph.clear();
      // set src cost_marker to 0.0
      Vertex current = graph.get(src);
      current.cost_marker = 0.0;
      open_queue.push(current);

      while (!open_queue.empty()) {
        // get node with lowest cost from the queue
        current = open_queue.top();
        open_queue.pop();
        // check if current node is destination node
        if (current.get_id() == dst) {
          success = true;
          break;
        }
        // check each neighbor of current vertex
        for (auto edge : current.neighbors()) {
          Vertex neighbor = graph.get(edge.destination);
          if (neighbor.on_closed_list) {
            // omit neighbors on closed list
            continue;
          }
          // update neighbor cost and set parent on path
          if (neighbor.cost_marker > current.cost_marker + edge.cost) {
            neighbor.cost_marker = current.cost_marker + edge.cost;
            neighbor.parent = current.get_id();
            open_queue.push(neighbor);
          }
        }
        // mark current as visited
        current.on_closed_list = true;
      }
      if (!success) {
        // the queue is empty, but we still have not succeded, which means
        // that src and dst are not on the same component!
        // We need to throw an error
        throw pathfinfing_error;
      }

      // prepare result
      vector<long> path;
      double cost = current.cost_marker;
      // backtrack to construct path
      while (current.parent != -1) {
        path.push_back(current.parent);
        current = graph.get(current.parent);
      }
      return tuple<vector<long>, double>{path, cost};
    }

    // calculates shortest path like find_path, but returns only the path cost
    double path_cost(long src, long dst) {
      tuple<vector<long>, double> path = find_path(src, dst);
      return get<1>(path);
    }

  private:
    // Private exception class that is thrown when a path could not be found
    class PathfindingError: public exception {
      virtual const char* what() const throw()
      {
        return "No path exists";
      }
    } pathfinfing_error;
};


// --------------------------
// ---------- MAIN ----------
// --------------------------

int main(void) {
  double avg_cost;

  // run first experiment with size=50, density=0.2
  ShortestPathExperiment experiment1(50, 0.2);
  avg_cost = experiment1.calculate_avg_path_cost();
  cout << "Average path cost is " << avg_cost << endl;

  // separate outputs
  cout << endl << "***" << endl << endl;

  // run second experiment with size=50, density=0.4
  ShortestPathExperiment experiment2(50, 0.4);
  avg_cost = experiment2.calculate_avg_path_cost();
  cout << "Average path cost is " << avg_cost << endl;

  return 0;
}
