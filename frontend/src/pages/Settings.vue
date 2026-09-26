<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({}); const saved = ref(false)
onMounted(async () => { s.value = await getJSON('/api/settings') })
async function saveDefault() {
  s.value = await putJSON('/api/settings', { default_orientation: s.value.default_orientation || 'vertical' })
  saved.value = true
}
</script>
<template>
  <div class="page"><h1>设置</h1>
  <label>默认贴向
    <select v-model="s.default_orientation" @change="saved=false">
      <option value="vertical">竖贴</option>
      <option value="horizontal">横贴</option>
    </select>
  </label>
  <button @click="saveDefault">保存</button>
  <span v-if="saved">已保存（仅影响之后的测算，不改写历史记录）</span>
  <pre>{{ s }}</pre></div>
</template>
