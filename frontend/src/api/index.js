import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

export const materialApi = {
  list: () => api.get('/materials'),
  detail: (id) => api.get(`/materials/${id}`),
  create: (data) => api.post('/materials', data),
  update: (id, data) => api.put(`/materials/${id}`, data),
  delete: (id) => api.delete(`/materials/${id}`),
  submit: (id) => api.post(`/materials/${id}/submit`),
  upload: (file) => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/materials/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
