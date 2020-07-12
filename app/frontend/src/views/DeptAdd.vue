<template>
  <div class="home">
    <AddDeptForm @deptadd="add">
    </AddDeptForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import AddDeptForm from '@/components/AddDept.vue';

export default {
  name: 'AddDept',
  components: {
    AddDeptForm,
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    add(data) {
      const path = 'dept/add_dept_json';
      const updat = data;
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then((response) => {
          alert(response.data.result);
        })
        .catch((error) => {
          alert(error.response.data.result);
          console.error(error);
        });
    },
  },
  created() {
    if (!this.$store.getters.isAuthenticated) {
      alert("Session expired. You have to login again");
      this.logout();
    }
  },
};
</script>
