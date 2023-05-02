package handlers

import (
	"fmt"
	"net/http"
	"sync"
)

var onlineNodeCount int
var numNodes int
var mu sync.Mutex

// NodeInfo represents information about an IPFS node
type NodeInfo struct {
	ID      string `json:"id"`
	Version string `json:"version"`
	Addr    string `json:"address"`
	Proto   string `json:"protocol"`
}

func NodesOnlineHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	fmt.Fprintf(w, "%d nodes online", numNodes)
}
func NodeConnectedHandler(w http.ResponseWriter, r *http.Request) {
	onlineNodeCount++
	fmt.Printf("Node connected. Online nodes: %d\n", onlineNodeCount)
}

func NodeDisconnectedHandler(w http.ResponseWriter, r *http.Request) {
	onlineNodeCount--
	fmt.Printf("Node disconnected. Online nodes: %d\n", onlineNodeCount)
}

func main() {
	http.HandleFunc("/nodes", HomeHandler)
	http.HandleFunc("/nodes-online", NodesOnlineHandler)
	http.ListenAndServe(":8081", nil)
}

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	numNodes++
	mu.Unlock()
	fmt.Fprintf(w, "Welcome to my website! Number of nodes online: %d", numNodes)
}
func LessHomeHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	numNodes--
	mu.Unlock()

}
