// Graph-related homeworks for C++ for C Programmers course
//
// This files contains code for two homeworks:
// - Homework 2: Dijkstra's algorithm
// - Homework 3: Minimum Spanning Tree
// - Homework 4: Play HEX game with random AI
//
// Code uses C++11 features extensively.
// Please, compile it with the --std=c++11 flag

#include <algorithm>
#include <fstream>
#include <iostream>
#include <limits>
#include <queue>
#include <random>
#include <string>
#include <tuple>
#include <unordered_set>
#include <vector>

using namespace std;


// -------------------
// Constant parameters
// -------------------

const long DEFAULT_GRAPH_SIZE = 50;
const double MIN_COST = 1.0;
const double MAX_COST = 10.0;
const double INF = numeric_limits<double>::infinity();

const string GAME_RULES = (
  "HEX GAME\n"
  "\n"
  "Rules:\n"
  "  - Each player places markers in turn, like in TIC-TAC-TOE\n"
  "  - BLUE player starts.\n"
  "  - RED player needs to connect upper and lower edges of the board.\n"
  "  - BLUE player needs to connect left and right edges of the board.\n"
  "\n"
);

enum class Color {NONE, RED, BLUE};

// Color enum should be printable
ostream& operator<< (ostream& out, Color color) {
  switch (color) {
    case Color::NONE:
      return out << ".";
    case Color::RED:
      return out << "R";
    case Color::BLUE:
      return out << "B";
  }
}


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


// -----------------
// Utility functions
// -----------------

// fix std:cin after unparseable input
// my OS demands multiple calls to ignore, clear and sync
void fix_cin() {
  cin.ignore();
  cin.clear();
  cin.sync();
  cin.ignore();
  cin.clear();
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
    Color color = Color::NONE;  // color for HEX game

  public:
    // public data members used as helpers by pathfinding algorithms
    double cost_marker = INF;  // stores vertex cost on currently calculated path
    bool on_closed_list = false;  // marks if vertex was visited on current run
    long parent = -1;  // id of vertex that leads to this on the shortest path

    Vertex() {}
    ~Vertex() {}

    long get_id(void) {
      return id;
    }

    void set_id(long new_id) {
      id = new_id;
    }

    Color get_color(void) {
      return color;
    }

    void set_color(Color new_color) {
      color = new_color;
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
    friend ostream& operator<< (ostream& out, Vertex vertex) {
      return out << "Vertex(" << vertex.size() << ")";
    };
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
      // cout << "Creating graph with " << size << " vertices" << endl;
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

    vector<Vertex> get_all() {
      return vertices;
    }

    long size(void) {
      return vertices.size();
    }

    // Calculates number of edges by iterating through all of graph's vertices
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

    // Generates edges corresponding to hex board of sqrt(size) size
    // Each edge is undirected and has an unit cost
    void generate_hex_edges(void) {
      int board_size = sqrt(size());
      for (int x = 0; x < board_size; ++x) {
        for (int y = 0; y < board_size; ++y) {
          int current = y * board_size + x;
          // add E connection
          if (x <= board_size) {
            vertices[current].add(Edge(1.0, current + 1));
            vertices[current + 1].add(Edge(1.0, current));
          }
          // add SE connection
          if (y <= board_size) {
            vertices[current].add(Edge(1.0, current + board_size));
            vertices[current + board_size].add(Edge(1.0, current));
          }
          // add SW connection
          if (x >= 0 && y <= board_size) {
            vertices[current].add(Edge(1.0, current + board_size - 1));
            vertices[current + board_size - 1].add(Edge(1.0, current));
          }
        }
      }
    }

    // adds an edge from src to dst with given cost
    void add_edge(const int src, const int dst, const double cost) {
      vertices[src].add(Edge(cost, dst));
    }

    friend ostream& operator<< (ostream& out, Graph & graph) {
      return out << "Graph(vertices=" << graph.size()
        << ", edges=" << graph.num_edges() << ")";
    }
};


// ----------------------
// Homework 2 & 3 Classes
// ----------------------

// Class responsible for creating a random graph with given size and density
// and calculating average shortest paths.
class GraphExperiment {
    Graph graph;

  public:
    // Constructor for random graph used by Homework 2
    GraphExperiment(const long size, const double density):graph(size) {
      graph.generate_random_edges(density);
    }
    // Constructor for loading graph from file used by Homework 3
    GraphExperiment(string filename):graph(0) {
      cout << "Loading file '" << filename << "'" << endl;
      ifstream input (filename);
      // read first line for graph size
      int size;
      input >> size;
      // create graph
      graph = Graph(size);
      // read rest of the file for edges
      while (!input.eof()) {
        int src, dst, cost;
        input >> src >> dst >> cost;
        graph.add_edge(src, dst, cost);
      }
    }
    ~GraphExperiment(){}

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

    // Calculate Minimum Spanning Tree using Kruskal's algorithm
    Graph mst() {
      cout << "Creating Minimum Spanning Tree" << endl;
      // create a list of all existing edges
      // define a touple of cost, src vertex and dst vertex
      typedef tuple<double, int, int> CostSrcDst;
      vector<CostSrcDst> edges;
      for (auto vertex : graph.get_all()) {
        for (auto edge : vertex.neighbors()) {
          if (vertex.get_id() > edge.destination) {
            // graph is undirected, but stores an edge object for each direction
            // we need to add only one direction to our list,
            // so we need to continue here to avoid data duplication
            continue;
          }
          // add CostSrcDst to the list
          edges.push_back(CostSrcDst(edge.cost, vertex.get_id(), edge.destination));
        }
      }
      // sort the list to be able to start with the shortest edges
      sort(edges.begin(), edges.end());
      // create a new graph object for the MST with the same size
      Graph mst (graph.size());
      // build MST in one pass through edges list
      int added_edges = 0;
      double total_cost = 0.0;
      cout << "Cost\tSrc\tDst" << endl;
      for (auto costsrcdst : edges) {
        double cost = get<0>(costsrcdst);
        Vertex src_vertex = graph.get(get<1>(costsrcdst));
        Vertex dst_vertex = graph.get(get<2>(costsrcdst));
        cout << cost << "\t" << src_vertex.get_id() << "\t" << dst_vertex.get_id() << endl;
        if (src_vertex.on_closed_list && dst_vertex.on_closed_list) {
          // this edge would create a cycle - we must ignore it
          continue;
        }
        // add edges both ways for undirected MST
        src_vertex.add(Edge(cost, dst_vertex.get_id()));
        dst_vertex.add(Edge(cost, src_vertex.get_id()));
        src_vertex.on_closed_list = true;
        dst_vertex.on_closed_list = true;
        added_edges += 1;
        total_cost += cost;
        if (added_edges == graph.size() - 1) {
          // early exit oportunity when MST is completed
          break;
        }
      }
      cout << "Total cost: " << total_cost << endl;
      return mst;
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


// Perform two experiments on undirected random graphs.
// Calculate average shortest paths for two 50-node graphs
// with edge density = 0.2 and 0.4
int homework2_dijkstra(void) {
  double avg_cost;

  // run first experiment with size=50, density=0.2
  GraphExperiment experiment1(50, 0.2);
  avg_cost = experiment1.calculate_avg_path_cost();
  cout << "Average path cost is " << avg_cost << endl;

  // separate outputs
  cout << endl << "***" << endl << endl;

  // run second experiment with size=50, density=0.4
  GraphExperiment experiment2(50, 0.4);
  avg_cost = experiment2.calculate_avg_path_cost();
  cout << "Average path cost is " << avg_cost << endl;

  return 0;
}


// Load graph from file and generate minimum span tree
int homework3_mst(string filename) {
  GraphExperiment experiment(filename);
  Graph mst = experiment.mst();
  return 0;
}


// ------------------
// Homework 4 Classes
// ------------------


class HexGame {
    Graph board;

    int move_x, move_y;  // stores current move coordinates



  public:
    // The constructor initializes board graph with size * size vertices
    HexGame(const int size):board(size * size) {
      board.generate_hex_edges();
    }
    ~HexGame() {}

    int size(void) {
      return sqrt(board.size());
    }

    // get board graph vertices by (X, Y) dimension
    Vertex& get(const int x, const int y) {
      return board.get(x + y * size());
    }

    // Start the HEX game
    int start(void) {
      Color player = Color::BLUE;  // BLUE player starts the game
      Color winner = Color::NONE;
      while (winner == Color::NONE) {  // MAIN GAME LOOP

        // ask for move_x and move_y
        if (player == Color::BLUE) {
          ask_player_for_move(player);
        } else {
          ask_random_ai_for_move(player);
        }

        // place color on specified field
        get(move_x, move_y).set_color(player);

        // switch players
        if (player == Color::BLUE) {
          player = Color::RED;
        } else {
          player = Color::BLUE;
        }

        // check winner
        winner = check_winner();
      }

      // print winner and exit
      show_UI();
      cout << "Player " << winner << " has won! Congratulations!!!" << endl;
      return 0;
    }

    // Ask human player for move.
    // It shows a user interface and scans stdin for move coordinates.
    // If there were any errors a message will be displayed and user
    // must repeat the process.
    void ask_player_for_move(Color player) {
      string error_message = "";
      while (true) {
        char separator;

        // user interface
        show_UI(error_message);
        cout << endl << (player == Color::BLUE ? "BLUE" : "RED");
        cout << ", please specify your move (ex. '3,5'):" << endl;

        // get input
        cin >> move_x >> separator >> move_y;

        // validate input
        if (cin.fail()) {
          fix_cin();
          error_message = "INCORRECT INPUT!";
          continue;
        }
        if (!(0 <= move_x && move_x < size()
              && 0 <= move_y && move_y < size()
              && separator == ',')) {
          error_message = "INCORRECT INPUT!";
          continue;
        }
        if (get(move_x, move_y).get_color() != Color::NONE) {
          error_message = "FIELD IS ALREADY OCCUPIED! Choose another one.";
          continue;
        }
        // move_x and move_y successfully set, we can break and return
        break;
      }
    }

    // Generates random moves until an empty field is found.
    // It is pretty efficient even if only few fields are left,
    // because it avoids full graph scan for empty fields.
    void ask_random_ai_for_move(Color player) {
      uniform_int_distribution<> random_move(0, size());
      do {
        move_x = random_move(r_engine);
        move_y = random_move(r_engine);
      } while (get(move_x, move_y).get_color() != Color::NONE);
    }

    // Displays User Interface
    void show_UI(string error_message="") {
      cout << string(50, '\n');  // clear screen
      cout << GAME_RULES;
      cout << error_message << endl << endl;  // display error message box
      cout << *this;  // print game board
    }

    // Checks which color won.
    // It looks for a BLUE path from left ot right edge
    // or a RED path from upper to lower edge.
    // If no winner is found it returns Color::NONE
    Color check_winner(void) {
      unordered_set<long> left_edge, right_edge, upper_edge, lower_edge;

      // find BLUE vertices on BLUE edges
      for (int y = 0; y < size(); ++y) {
        if (get(0, y).get_color() == Color::BLUE) {
          left_edge.insert(get(0, y).get_id());
        }
        if (get(size() - 1, y).get_color() == Color::BLUE) {
          right_edge.insert(get(size() - 1, y).get_id());
        }
      }
      // check if edges are connected
      if (exists_path(left_edge, right_edge, Color::BLUE)) {
        return Color::BLUE;
      }

      // find RED vertices on RED edges
      for (int x = 0; x < size(); ++x) {
        if (get(x, 0).get_color() == Color::RED) {
          upper_edge.insert(get(x, 0).get_id());
        }
        if (get(x, size() - 1).get_color() == Color::RED) {
          lower_edge.insert(get(x, size() - 1).get_id());
        }
      }
      // check if edges are connected
      if (exists_path(upper_edge, lower_edge, Color::RED)) {
        return Color::RED;
      }

      // no winner found
      return Color::NONE;
    }

    // Check if path exists from a set of vertices to a set of vertices.
    // Uses modified Dijkstra's algorithm that allows a set of sources
    // and a set of destinations and is not interested in shortest path,
    // but only wether a path exists.
    bool exists_path(const unordered_set<long> &src, const unordered_set<long> &dst, Color color) {
      if (src.empty() || dst.empty()) {
        return false;
      }
      // prepare a priority queue for the algorithm
      priority_queue<Vertex, vector<Vertex>, OrderByCostMarker> open_queue;
      bool success = false;
      // clear board of pathfinding markers
      board.clear();
      // set src vertices cost_marker to 0.0 and add them to open queue
      for (long vertex: src) {
        Vertex current = board.get(vertex);
        current.cost_marker = 0.0;
        open_queue.push(current);
      }

      while (!open_queue.empty()) {
        // get node with lowest cost from the queue
        Vertex current = open_queue.top();
        open_queue.pop();
        // check if current node is destination node
        if (dst.find(current.get_id()) != dst.end()) {
          success = true;
          break;
        }
        // check each neighbor of current vertex
        for (auto edge: current.neighbors()) {
          Vertex neighbor = board.get(edge.destination);
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
      return success;
    }

    // print game board in ASCII art fashion
    friend ostream& operator<< (ostream& out, HexGame &game) {
      int size = game.size();

      // print column labels
      out << "   ";
      for (int x = 0; x < size; ++x) {
        out << ((x < 10) ? " ": "") << x << "  ";
      }
      out << endl;

      // print nodes and edges
      for (int y = 0; y < size; ++y) {
        // print row label
        out << string(y * 2, ' ');
        out << ((y < 10) ? " ": "") << y << " ";

        // print nodes
        for (int x = 0; x < size; ++x) {
          out << " " << game.get(x, y).get_color();
          if (x < size - 1) {
            out << " -";
          }
        }
        out << endl;

        // draw SW and SE edges
        if (y < size - 1) {
          out << string(5 + y * 2, ' ');
          for (int x = 0; x < size - 1; ++x) {
            out << "\\ / ";
          }
          out << "\\" << endl;
        }
      }
      return out;
    }
};


// Homework 4: Run HEX game without AI
//
// Expectations:
// - Be able to draw the board using ASCII symbols and a given size,
//   such as 7 by 7 or 11 by 11.
// - Input a move and determine if a move is legal.
// - Determine who won.
int homework4_hex() {
  // ask for board size
  int size = 0;
  while (size < 4 || size > 11) {
    cout << "Specify board size (from 4 to 11):" << endl;
    if (!(cin >> size)) {
      fix_cin();
    }
  }
  // create and start game
  return HexGame(size).start();
}

// --------------------------
// ---------- MAIN ----------
// --------------------------

int main(int argc, const char* argv[]) {
  // Uncomment for Homework 2
  /*
  return homework2_dijkstra();
  */

  // Uncomment for homework 3
  /*
  if (argc != 2) {
    cout << "Usage: " << argv[0] << " <graph_filename>" << endl;
    return 1;
  }
  return homework3_mst(argv[1]);
  */

  // Uncomment for homework 4
  return homework4_hex();
}
