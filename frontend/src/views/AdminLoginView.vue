<template>
  <div class="admin-login-page">
    <div class="login-card">
      <div class="logo-area">
        <div class="logo-icon">🛡️</div>
        <h1>管理员后台</h1>
        <p class="subtitle">仅限授权人员访问</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="field-group">
          <label for="admin-password">管理员密码</label>
          <div class="input-wrapper">
            <span class="input-icon">🔒</span>
            <input
              id="admin-password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="请输入管理员密码"
              autocomplete="current-password"
              :disabled="loading"
            />
            <button
              type="button"
              class="toggle-btn"
              @click="showPassword = !showPassword"
              tabindex="-1"
            >
              {{ showPassword ? "🙈" : "👁️" }}
            </button>
          </div>
        </div>

        <div v-if="errorMsg" class="error-banner">
          ⚠️ {{ errorMsg }}
        </div>

        <button
          id="admin-login-btn"
          type="submit"
          class="login-btn"
          :disabled="loading || !password"
        >
          <span v-if="loading" class="spinner"></span>
          <span v-else>进入后台</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAdminStore } from "../stores/admin";

const router = useRouter();
const adminStore = useAdminStore();

const password = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMsg = ref("");

async function handleLogin() {
  if (!password.value) return;
  loading.value = true;
  errorMsg.value = "";
  try {
    await adminStore.login(password.value);
    router.push("/admin");
  } catch (err) {
    const msg = err?.response?.data?.detail || "密码错误，请重试";
    errorMsg.value = msg;
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  font-family: "Inter", "PingFang SC", sans-serif;
}

.login-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 24px;
  padding: 48px 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 32px 80px rgba(0, 0, 0, 0.5);
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

.logo-area {
  text-align: center;
  margin-bottom: 36px;
}

.logo-icon {
  font-size: 3rem;
  margin-bottom: 12px;
  filter: drop-shadow(0 0 16px rgba(139, 92, 246, 0.6));
}

h1 {
  color: #fff;
  font-size: 1.6rem;
  font-weight: 700;
  margin: 0 0 6px;
  letter-spacing: -0.5px;
}

.subtitle {
  color: rgba(255, 255, 255, 0.45);
  font-size: 0.875rem;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  font-size: 1rem;
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 14px 44px 14px 42px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

.input-wrapper input:focus {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
}

.input-wrapper input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.input-wrapper input:disabled {
  opacity: 0.5;
}

.toggle-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 4px;
  line-height: 1;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.toggle-btn:hover { opacity: 1; }

.error-banner {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.35);
  border-radius: 10px;
  color: #fca5a5;
  padding: 12px 16px;
  font-size: 0.875rem;
  animation: shake 0.3s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  75% { transform: translateX(6px); }
}

.login-btn {
  padding: 15px;
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s;
  box-shadow: 0 8px 24px rgba(109, 40, 217, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(109, 40, 217, 0.5);
}

.login-btn:active:not(:disabled) {
  transform: translateY(0);
}

.login-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
