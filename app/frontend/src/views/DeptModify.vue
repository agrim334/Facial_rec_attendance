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
      const path = 'http://localhost:5000/depts/modify_dept_json';
      axios.post(path, { old: this.dept, new: deptdat })
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
