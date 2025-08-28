"use client"

import React, { useState } from "react";
import { RefreshCw, Newspaper } from "lucide-react";

interface NewsItem {
  id: number;
  title: string;
  source: string;
  author: string;
  description: string;
  publishedAt: string;
  url: string;
  urlToImage: string;
}

const NewsApp: React.FC = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const retryLimit: number = parseInt(process.env.NEXT_MAX_RETRY_LOG_NEWS ?? "3", 10);

  // Invocación de función de logueo con reintento
  const writeLog = async (counter: number = 0): Promise<void> => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_GET_NEWS_BASE}/api/LogAccess`, { method: 'POST' });
      if (!response.ok && counter < retryLimit) {
        await writeLog(counter + 1)
      }
    } catch (error) {
      await writeLog(counter + 1)
    }
  }


  const loadNews = async (): Promise<void> => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_GET_NEWS_BASE}/api/GetNews`);
      writeLog()
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: NewsItem[] = await response.json();
      setNews(data);

    } catch (err) {
      setError("Error al cargar las noticias. Por favor, intenta nuevamente.");
      console.error("Error loading news:", err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString("es-ES", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };


  const leerMas = (url: string) => {
    window.open(url, "_blank", "noopener,noreferrer");
  }


  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Newspaper className="w-12 h-12 text-indigo-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-800">
              Titulares de Noticias
            </h1>
          </div>
          <p className="text-gray-600 text-lg">
            ¡Mantenete informado con las últimas noticias!
          </p>
        </div>

        {/* Load Button */}
        <div className="text-center mb-8">
          <button
            onClick={loadNews}
            disabled={loading}
            className={`
              inline-flex items-center px-6 py-3 text-white font-semibold rounded-lg
              transition-all duration-200 transform hover:scale-105 focus:outline-none
              focus:ring-4 focus:ring-indigo-300 shadow-lg
              ${loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700 active:scale-95"
              }
            `}
          >
            <RefreshCw
              className={`w-5 h-5 mr-2 ${loading ? "animate-spin" : ""}`}
            />
            {loading ? "Cargando noticias..." : "Cargar Noticias"}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            <p className="font-medium">Error:</p>
            <p>{error}</p>
          </div>
        )}

        {/* News List */}
        {news.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
              Últimas Noticias ({news.length})
            </h2>

            <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-2">
              {news.map((item) => (
                <div
                  key={item.id}
                  className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6 border border-gray-200"
                >
                  <div className="flex flex-col h-full">
                    {/* Imagen de la noticia */}
                    {item.urlToImage && (
                      <img
                        src={item.urlToImage}
                        alt={item.title}
                        className="w-full h-48 mb-4 object-cover"
                      />
                    )}

                    <h3 className="text-lg font-semibold text-gray-800 mb-3 line-clamp-2">
                      {item.title}
                    </h3>

                    <div className="flex-grow"></div>

                    <div className="flex justify-between items-center text-sm text-gray-600 mt-4">
                      <span className="font-medium bg-indigo-100 text-indigo-800 px-2 py-1 rounded">
                        {item.source}
                      </span>
                      <span>{formatDate(item.publishedAt)}</span>
                    </div>

                    <button
                      onClick={() => leerMas(item.url)}
                      className="mt-3 text-indigo-600 hover:text-indigo-800 font-medium text-sm transition-colors duration-200 cursor-pointer">
                      Leer más →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && news.length === 0 && !error && (
          <div className="text-center py-12">
            <Newspaper className="w-24 h-24 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              No hay noticias cargadas
            </h3>
            <p className="text-gray-500">
              Haz clic en &quot;Cargar Noticias&quot; para ver los últimos titulares
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default NewsApp;
