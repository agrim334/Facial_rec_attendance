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
    updaterec(deptdat) {
      alert(deptdat);
      const path = 'dept/modify_dept_json';
      const updat = { old: this.dept, new: deptdat };
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then(() => {
          console.log('done');
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
