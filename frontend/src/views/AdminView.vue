<template>
  <div class="admin-page">
    <!-- 顶部导航 -->
    <header class="admin-header">
      <div class="header-left">
        <span class="header-icon">🛡️</span>
        <span class="header-title">管理员后台</span>
      </div>
      <button id="admin-logout-btn" class="logout-btn" @click="handleLogout">退出登录</button>
    </header>

    <!-- 统计卡片 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.totalUsers }}</div>
          <div class="stat-label">注册用户</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.totalRecords }}</div>
          <div class="stat-label">改写记录</div>
        </div>
      </div>
    </div>

    <!-- 用户列表 -->
    <section class="section">
      <div class="section-header">
        <h2>用户列表</h2>
        <span class="badge">共 {{ stats.totalUsers }} 人</span>
      </div>

      <div v-if="usersLoading" class="loading-row">
        <span class="spinner"></span> 加载中…
      </div>
      <div v-else-if="users.length === 0" class="empty-row">暂无用户</div>
      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>邮箱</th>
              <th>注册时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td class="mono">{{ u.id }}</td>
              <td>{{ u.username }}</td>
              <td class="email">{{ u.email }}</td>
              <td class="mono">{{ formatDate(u.created_at) }}</td>
              <td>
                <button
                  class="del-btn"
                  :id="`del-user-${u.id}`"
                  @click="deleteUser(u.id, u.username)"
                  :disabled="deletingUserId === u.id"
                >
                  {{ deletingUserId === u.id ? "删除中…" : "删除" }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 用户分页 -->
      <div class="pagination" v-if="stats.totalUsers > usersPageSize">
        <button class="page-btn" :disabled="usersPage === 1" @click="usersPage--; fetchUsers()">上一页</button>
        <span class="page-info">第 {{ usersPage }} 页</span>
        <button class="page-btn" :disabled="usersPage * usersPageSize >= stats.totalUsers" @click="usersPage++; fetchUsers()">下一页</button>
      </div>
    </section>

    <!-- 改写记录列表 -->
    <section class="section">
      <div class="section-header">
        <h2>改写记录</h2>
        <span class="badge">共 {{ stats.totalRecords }} 条</span>
      </div>

      <div v-if="recordsLoading" class="loading-row">
        <span class="spinner"></span> 加载中…
      </div>
      <div v-else-if="records.length === 0" class="empty-row">暂无记录</div>
      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户</th>
              <th>原文摘要</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in records" :key="r.id">
              <td class="mono">{{ r.id }}</td>
              <td>{{ r.username }}</td>
              <td class="preview">{{ r.source_preview }}</td>
              <td class="mono">{{ formatDate(r.created_at) }}</td>
              <td>
                <button
                  class="del-btn"
                  :id="`del-record-${r.id}`"
                  @click="deleteRecord(r.id)"
                  :disabled="deletingRecordId === r.id"
                >
                  {{ deletingRecordId === r.id ? "删除中…" : "删除" }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 记录分页 -->
      <div class="pagination" v-if="stats.totalRecords > recordsPageSize">
        <button class="page-btn" :disabled="recordsPage === 1" @click="recordsPage--; fetchRecords()">上一页</button>
        <span class="page-info">第 {{ recordsPage }} 页</span>
        <button class="page-btn" :disabled="recordsPage * recordsPageSize >= stats.totalRecords" @click="recordsPage++; fetchRecords()">下一页</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import http from "../api/http";
import { useAdminStore } from "../stores/admin";

const router = useRouter();
const adminStore = useAdminStore();

// ——— 状态 ———
const users = ref([]);
const records = ref([]);
const usersLoading = ref(false);
const recordsLoading = ref(false);
const deletingUserId = ref(null);
const deletingRecordId = ref(null);
const usersPage = ref(1);
const usersPageSize = 20;
const recordsPage = ref(1);
const recordsPageSize = 20;
const stats = ref({ totalUsers: 0, totalRecords: 0 });

// ——— 工具 ———
function adminHeaders() {
  return { Authorization: `Bearer ${adminStore.token}` };
}

function formatDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleString("zh-CN", { hour12: false });
}

// ——— 数据获取 ———
async function fetchUsers() {
  usersLoading.value = true;
  try {
    const { data } = await http.get("/admin/users", {
      params: { page: usersPage.value, page_size: usersPageSize },
      headers: adminHeaders(),
    });
    users.value = data.items;
    stats.value.totalUsers = data.total;
  } catch {
    /* ignore */
  } finally {
    usersLoading.value = false;
  }
}

async function fetchRecords() {
  recordsLoading.value = true;
  try {
    const { data } = await http.get("/admin/records", {
      params: { page: recordsPage.value, page_size: recordsPageSize },
      headers: adminHeaders(),
    });
    records.value = data.items;
    stats.value.totalRecords = data.total;
  } catch {
    /* ignore */
  } finally {
    recordsLoading.value = false;
  }
}

// ——— 删除操作 ———
async function deleteUser(id, name) {
  if (!confirm(`确定删除用户「${name}」？此操作不可撤销，该用户所有改写记录也会同步删除。`)) return;
  deletingUserId.value = id;
  try {
    await http.delete(`/admin/users/${id}`, { headers: adminHeaders() });
    await Promise.all([fetchUsers(), fetchRecords()]);
  } catch (e) {
    alert(e?.response?.data?.detail || "删除失败");
  } finally {
    deletingUserId.value = null;
  }
}

async function deleteRecord(id) {
  if (!confirm(`确定删除记录 #${id}？`)) return;
  deletingRecordId.value = id;
  try {
    await http.delete(`/admin/records/${id}`, { headers: adminHeaders() });
    await fetchRecords();
    stats.value.totalRecords--;
  } catch (e) {
    alert(e?.response?.data?.detail || "删除失败");
  } finally {
    deletingRecordId.value = null;
  }
}

// ——— 退出登录 ———
function handleLogout() {
  adminStore.logout();
  router.push("/admin/login");
}

onMounted(() => {
  fetchUsers();
  fetchRecords();
});
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #0d0221 0%, #1a0533 50%, #0d1117 100%);
  font-family: "Inter", "PingFang SC", sans-serif;
  color: #e2e8f0;
  padding-bottom: 60px;
}

/* ——— 顶部导航 ——— */
.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 40px;
  background: rgba(255, 255, 255, 0.04);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon { font-size: 1.4rem; }

.header-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.3px;
}

.logout-btn {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 8px 18px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: background 0.2s, border-color 0.2s;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.25);
  border-color: rgba(239, 68, 68, 0.5);
}

/* ——— 统计卡片 ——— */
.stats-row {
  display: flex;
  gap: 20px;
  padding: 32px 40px 0;
}

.stat-card {
  flex: 1;
  max-width: 220px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(109, 40, 217, 0.08));
  border: 1px solid rgba(139, 92, 246, 0.25);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(139, 92, 246, 0.2);
}

.stat-icon { font-size: 2rem; }

.stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #fff;
  line-height: 1;
}

.stat-label {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
  margin-top: 4px;
}

/* ——— 区块 ——— */
.section {
  margin: 32px 40px 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-header h2 {
  color: #fff;
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
}

.badge {
  background: rgba(139, 92, 246, 0.2);
  border: 1px solid rgba(139, 92, 246, 0.35);
  color: #c4b5fd;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.78rem;
}

/* ——— 表格 ——— */
.table-wrapper {
  overflow-x: auto;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.data-table thead tr {
  background: rgba(255, 255, 255, 0.05);
}

.data-table th {
  padding: 14px 16px;
  text-align: left;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.data-table tbody tr {
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  transition: background 0.15s;
}

.data-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.03);
}

.data-table td {
  padding: 14px 16px;
  color: #cbd5e1;
}

.data-table td.mono {
  font-family: "JetBrains Mono", "Fira Code", monospace;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.45);
}

.data-table td.email {
  color: #94a3b8;
  font-size: 0.83rem;
}

.data-table td.preview {
  color: #94a3b8;
  font-size: 0.83rem;
  max-width: 280px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ——— 删除按钮 ——— */
.del-btn {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: #fca5a5;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
  transition: background 0.2s, border-color 0.2s;
}

.del-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.25);
  border-color: rgba(239, 68, 68, 0.45);
}

.del-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ——— 分页 ——— */
.pagination {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
  justify-content: flex-end;
}

.page-btn {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #e2e8f0;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.12);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  color: rgba(255, 255, 255, 0.45);
  font-size: 0.85rem;
}

/* ——— 加载 / 空状态 ——— */
.loading-row, .empty-row {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255, 255, 255, 0.35);
  padding: 40px;
  justify-content: center;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .admin-header { padding: 16px 20px; }
  .stats-row { padding: 20px 20px 0; flex-wrap: wrap; }
  .section { margin: 24px 20px 0; }
  .stat-card { max-width: none; }
}
</style>
