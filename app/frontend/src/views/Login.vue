<template>
  <div class="home">
    <LogForm></LogForm>
  </div>
</template>

<script>
// @ is an alias to /src
import LogForm from '@/components/LogForm.vue';

export default {
  name: 'Form',
  components: {
    LogForm,
  },
};
</script>
