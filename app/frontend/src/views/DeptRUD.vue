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
      const path = 'http://localhost:5000/dept/delete_dept_json';
      axios.post(path, deptdat.id)
        .then(() => {
          this.getDept();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getDept() {
      const path = 'http://localhost:5000/dept/check_dept_json';
      axios.get(path)
        .then((res) => {
          this.depts = res.data.records;
          for (let i = 0; i < this.depts.length; i += 1) {
            this.depts[i].actions = '';
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
