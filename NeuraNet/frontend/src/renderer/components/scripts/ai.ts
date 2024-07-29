import ollama from 'ollama'



export async function chat(): Promise<any> {
  const response = await ollama.chat({
    model: 'llama2',
    messages: [{ role: 'user', content: 'Why is the sky blue?' }],
  })
  console.log(response.message.content)
}
