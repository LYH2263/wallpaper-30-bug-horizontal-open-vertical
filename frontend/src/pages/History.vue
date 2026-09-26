<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
const orientLabel = (r) => r.result?.orientation === 'horizontal' ? '横贴' : '竖贴'
</script>
<template>
  <div class="page"><h1>记录</h1>
  <ul>
    <li v-for="r in items" :key="r.id">
      {{ r.wall_name }} → {{ r.result?.rolls }} 卷 · {{ orientLabel(r) }} · {{ r.result?.drops }} 条
      · drop {{ r.result?.drop_len_m }}m · 每卷 {{ r.result?.strips_per_roll }} 条
    </li>
  </ul>
  <p class="hint">开放视图保留贴向标签，条带与卷数按列表接口返回。</p>
  </div>
</template>
