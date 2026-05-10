<template>
  <div id="app">
    <header class="app-header">
      <h1>取水许可材料智能审查系统</h1>
      <nav>
        <router-link to="/">材料列表</router-link>
        <router-link to="/create">新建材料</router-link>
      </nav>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Microsoft YaHei', sans-serif; background: #f5f7fa; color: #333; }
.app-header {
  background: #1a73e8;
  color: white;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.app-header h1 { font-size: 20px; }
.app-header nav a {
  color: white;
  margin-left: 24px;
  text-decoration: none;
  font-size: 15px;
}
.app-header nav a:hover { text-decoration: underline; }
.app-header nav a.router-link-active { font-weight: bold; }
.app-main { max-width: 1200px; margin: 24px auto; padding: 0 16px; }
</style>
