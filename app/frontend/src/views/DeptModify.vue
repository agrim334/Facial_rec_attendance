<template>
  <div class="home">
    <ModifyDeptForm :deptrec = 'dept' @updrec='updaterec'> </ModifyDeptForm>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import ModifyDeptForm from '@/components/ModifyDept.vue';

export default {
  name: 'DeptModify',
  props: {
    dept: Array,
  },
  components: {
    ModifyDeptForm,
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    updaterec(deptdat) {
      if (!this.$store.getters.isAuthenticated) {
        alert("Session expired. You have to login again");
        this.logout();
      }
      else {
        const path = 'dept/modify_dept_json';
        const updat = { old: this.dept, new: deptdat };
        this.$store.dispatch('authrequest', { url: path, data: updat })
          .then((response) => {
            alert(response.data.result);
            console.log(response);
          })
          .catch((error) => {
            alert(error.response.data.result);
            console.error(error);
          });
      }
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
