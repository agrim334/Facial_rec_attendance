<template>
  <div id="modifydept-form">
    <b-form @submit.prevent="handle">

    <label>Department ID</label>
    <b-input :state='depidstate' placeholder = "Enter Department ID"
    v-model = 'moddept.id' ></b-input>
    <br>

    <label>Department name</label>
    <b-input :state='depnstate' placeholder = "Enter Department name"
    v-model = 'moddept.name' ></b-input>
    <br>

    <b-button type="submit"> Modify Department </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'ModifyDeptForm',
  props: { deptrec: Array },
  data() {
    return {
      moddept: {
        id: this.deptrec.id || '',
        name: this.deptrec.name || '',
      },
    };
  },
  computed: {
    depidstate() {
      return this.moddept.id.length > 0;
    },
    depnstate() {
      return this.moddept.name.length > 0;
    },
  },
  methods: {
    validate() {
      let f = 0;
      if (this.moddept.id === null || this.moddept.id === '') {
        alert('fill dept id');
        f = 1;
      }
      if (this.moddept.name === null || this.moddept.name === '') {
        alert('fill dept name');
        f = 1;
      }
      if (f === 0) {
        this.$emit('updrec', this.moddept);
      }
    },
  },
};
</script>
