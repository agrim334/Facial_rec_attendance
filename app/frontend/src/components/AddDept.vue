<template>
  <div id="adddept-form">
    <b-form @submit.prevent="handle">
    <label>Department ID</label>
    <b-input :state='didstate' placeholder = "Enter Department ID"
    v-model = 'dept.id' >
    </b-input>
    <br>

    <label>Department name</label>
    <b-input :state='dnstate' placeholder = "Enter Department name"
    v-model = 'dept.name' ></b-input>
    <br>

    <b-button type="submit"> Add Department </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'AddDeptForm',
  data() {
    return {
      dept: {
        id: '', name: '',
      },
    };
  },
  computed: {
    didstate() {
      return this.dept.id.length > 0;
    },
    dnstate() {
      return this.dept.name.length > 0;
    },
  },
  methods: {
    handle() {
      let f = 0;
      if (this.dept.id === null || this.dept.id === '') {
        alert('fill dept id');
        f = 1;
      }
      if (this.dept.name === null || this.dept.name === '') {
        alert('fill dept name');
        f = 1;
      }
      if (f === 0) {
        this.$emit('deptadd', this.dept);
      }
    },
  },
};
</script>
