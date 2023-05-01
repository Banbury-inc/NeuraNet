package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"mymodule/web/api/handlers"
	"net/http"
	"path/filepath"
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

	http.HandleFunc("/upload", handlers.UploadHandler)
	http.HandleFunc("/download", handlers.DownloadHandler)
	http.HandleFunc("/nodes-online", handlers.NodesOnlineHandler)
	http.HandleFunc("/nodes", handlers.HomeHandler)
	http.HandleFunc("/lessnodes", handlers.LessHomeHandler)

	// Start server
	log.Println("Starting server on :8081")
	if err := http.ListenAndServe(":8081", nil); err != nil {
		log.Fatalf("Error starting server: %v", err)
	}
}
