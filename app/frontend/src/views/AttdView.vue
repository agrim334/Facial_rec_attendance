<template>
  <div class="home">
    <UserTable></UserTable>
  </div>
</template>

<script>
// @ is an alias to /src
import UserTable from '@/components/UserTable.vue';

export default {
  name: 'Table',
  components: {
    UserTable,
  },
};
</script>
