import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [prompt, setPrompt] = useState("")
  const [response, setResponse] = useState("")
  const [loading, setLoading] = useState(false)

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const res = await axios.post("http://localhost:8000/generate", {
        prompt: prompt
      })
      setResponse(res.data.result)
    } catch (error) {
      console.error(error)
      setResponse("Erreur lors de la génération.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-4">SmartSaaS - Générateur IA</h1>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="w-full max-w-xl p-2 border rounded mb-4"
        rows={4}
        placeholder="Entrez votre prompt ici..."
      />
      <button
        onClick={handleGenerate}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? "Génération..." : "Générer"}
      </button>
      {response && (
        <div className="mt-6 p-4 bg-white rounded shadow max-w-xl w-full">
          <h2 className="font-semibold mb-2">Résultat :</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  )
}