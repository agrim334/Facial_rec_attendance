<template>
  <div class="home">
  <DeptRec :depts='depts' @updrec='updaterec' @delrec='deleterec'>
  </DeptRec>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import DeptRec from '../components/RUDDept.vue';

export default {
  name: 'DeptTable',
  props: {
    depts: Array,
  },
  components: {
    DeptRec,
  },
  methods: {
    updaterec(deptdat) {
      this.$router.push({ name: 'DeptModify', params: { dept: deptdat } });
    },
    deleterec(deptdat) {
      const path = 'dept/delete_dept_json';
      this.$store.dispatch('authrequest', { url: path, data: deptdat.id })
        .then(() => {
          this.getDept();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getDept() {
      const path = 'dept/check_dept_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((res) => {
          this.depts = res.data.records;
          if (this.$store.state.userrole === 'Admin') {
            for (let i = 0; i < this.depts.length; i += 1) {
              this.depts[i].actions = '';
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getDept();
  },
};
</script>
