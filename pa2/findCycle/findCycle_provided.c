#include "../graphutils.h"

// A program to find a cycle in a directed graph

// You may use DFS or BFS as needed
/* ... */

int main ( int argc, char* argv[] ) {

    // READ INPUT FILE TO CREATE GRAPH ADJACENCY LIST
    AdjacencyListNode* adjacencyList;
    /* ... */

    bool isCyclic = false;
    for (unsigned source=0; source<graphNodeCount; source++) {
        /* ... */
    }

    if (!isCyclic) { printf("DAG\n"); }

    freeAdjList ( graphNodeCount, adjacencyList );
    return EXIT_SUCCESS;
}
