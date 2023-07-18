package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"mymodule/web/api/handlers"
	"net/http"
	"os"
	"path/filepath"

	"github.com/fsnotify/fsnotify"
)

func main() {
	// Serve static files
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Set up templates
	templates, err := template.ParseGlob(filepath.Join("web/ui/templates", "*.html"))
	if err != nil {
		log.Fatalf("Error parsing templates: %v", err)
	}

	// Set up routes
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/" || r.URL.Path == "/home.html" {
			data := struct {
				Title string
			}{
				Title: "Home",
			}
			if err := templates.ExecuteTemplate(w, "base.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else if r.URL.Path == "/signup.html" {
			data := struct {
				Title string
			}{
				Title: "Signup",
			}
			if err := templates.ExecuteTemplate(w, "signup.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else if r.URL.Path == "/upload.html" {
			data := struct {
				Title string
			}{
				Title: "Upload",
			}
			if err := templates.ExecuteTemplate(w, "upload.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else if r.URL.Path == "/download.html" {
			data := struct {
				Title string
			}{
				Title: "Download",
			}
			if err := templates.ExecuteTemplate(w, "download.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else if r.URL.Path == "/nodeslist.html" {
			data := struct {
				Title string
			}{
				Title: "Nodes",
			}
			if err := templates.ExecuteTemplate(w, "nodeslist.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else if r.URL.Path == "/file.html" {
			data := struct {
				Title string
			}{
				Title: "Files",
			}
			if err := templates.ExecuteTemplate(w, "file.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else {
			// Serve the file content when a link is clicked
			filePath := filepath.Join("static", r.URL.Path)
			fileContent, err := ioutil.ReadFile(filePath)
			if err != nil {
				http.Error(w, fmt.Sprintf("Error reading file: %v", err), http.StatusInternalServerError)
				return
			}
			data := struct {
				Title string
				Body  template.HTML
			}{
				Title: r.URL.Path,
				Body:  template.HTML(fileContent),
			}
			if err := templates.ExecuteTemplate(w, "base.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		}
	})

	http.HandleFunc("/download", handlers.DownloadHandler)
	http.HandleFunc("/nodes-online", handlers.NodesOnlineHandler)
	http.HandleFunc("/nodes", handlers.HomeHandler)
	http.HandleFunc("/lessnodes", handlers.LessHomeHandler)
	http.HandleFunc("/addnode", handlers.CreateNodeHandler)
	http.HandleFunc("/nodesdata", handlers.CreateNodeHandler)
	http.HandleFunc("/files", handlers.LogFiles)
	http.HandleFunc("/disconnect", handlers.DisconnectAllPeersHandler)
	http.HandleFunc("/countpeers", handlers.CountPeersHandler)
	http.HandleFunc("/listpeers", handlers.ListofPeersHandler)
	http.HandleFunc("/listfiles", handlers.ListFilesHandler)
	http.HandleFunc("/upload", handlers.UploadHandler)

	// Start server
	log.Println("Starting server on :8081")
	go func() {
		if err := http.ListenAndServe(":8081", nil); err != nil {
			log.Fatalf("Error starting server: %v", err)
		}
	}()

	// Create a file watcher
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal(err)
	}
	defer watcher.Close()

	// Watch for changes in the current directory and its subdirectories
	err = filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return watcher.Add(path)
		}
		return nil
	})
	if err != nil {
		log.Fatal(err)
	}

	// Watch for file changes and restart the server
	for {
		select {
		case event, ok := <-watcher.Events:
			if !ok {
				return
			}
			log.Println("event:", event)
			if event.Op&fsnotify.Write == fsnotify.Write {
				log.Println("modified file:", event.Name)
				// Restart the server by killing the current process and starting a new one
				os.Exit(0)
				// Start server
				log.Println("Starting server on :8081")
				go func() {
					if err := http.ListenAndServe(":8081", nil); err != nil {
						log.Fatalf("Error starting server: %v", err)
					}
				}()

			}
		case err, ok := <-watcher.Errors:
			if !ok {
				return
			}
			log.Println("error:", err)
		}
	}
}
