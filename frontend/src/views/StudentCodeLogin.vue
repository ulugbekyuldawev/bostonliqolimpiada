<template>
  <div class="student-entry-page olympiad-entry world-entry solo-entry">
    <div class="entry-orb entry-orb-one"></div>
    <div class="entry-orb entry-orb-two"></div>
    <div class="entry-orb entry-orb-three"></div>

    <section class="world-hero-shell solo-shell">
      <div class="student-card entry-card world-login-card">
        <div class="entry-top compact">
          <span class="entry-badge">Student access</span>
        </div>

        <h2>Testga kirish</h2>
        <p class="entry-subtitle">Admin bergan 6 xonali status code’ni kiriting.</p>

        <form @submit.prevent="startExam" class="code-form entry-form">
          <label class="code-label">
            Status code
            <input
              v-model="code"
              maxlength="6"
              minlength="6"
              inputmode="numeric"
              placeholder="582914"
              required
            />
          </label>
          <button class="primary-btn entry-start-btn" :disabled="loading">
            {{ loading ? 'Tekshirilmoqda...' : 'Testni boshlash' }}
          </button>
        </form>

        <p v-if="error" class="error-box">{{ error }}</p>

        <RouterLink to="/admin/login" class="admin-login-link entry-admin-link">
          Admin panelga kirish
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/axios'

const router = useRouter()
const code = ref('')
const loading = ref(false)
const error = ref('')

function cleanCode(value) {
  return String(value || '').trim()
}

async function startExam() {
  loading.value = true
  error.value = ''
  try {
    const finalCode = cleanCode(code.value)
    // Progressni o'chirmaymiz: bola testdan chiqib ketib qayta kirsa,
    // javoblari va vaqt hisoblanishi birinchi boshlagan joyidan davom etishi kerak.
    // Vaqt backenddagi student.started_at bo'yicha yuradi, qayta kirganda 30/10 daqiqadan
    // boshidan boshlanib ketmaydi.
    sessionStorage.removeItem('exam_payload')
    const res = await api.post('/exam/start/', { code: finalCode })
    sessionStorage.setItem('exam_payload', JSON.stringify({
      ...res.data,
      code: finalCode,
    }))
    router.push('/exam')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Code xato yoki oldin ishlatilgan.'
  } finally {
    loading.value = false
  }
}
</script>
