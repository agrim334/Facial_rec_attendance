<template>
  <div id="coursemod-form">
    <b-form @submit.prevent="validate">
    <label>Course ID</label>
    <b-input :state='cidstate' placeholder = "Enter Course ID"
    v-model = 'modcourse.id' >
    </b-input>
    <br>

    <label>Course name</label>
    <b-input :state='cnstate' placeholder = "Enter Course name"
    v-model = 'modcourse.name' ></b-input>
    <br>

    <b-button type="submit"> Modify Course </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'ModifyCourseForm',
  props: { courserec: Array },
  data() {
    return {
      modcourse: {
        id: this.courserec.id || '',
        name: this.courserec.name || '',
      },
    };
  },
  computed: {
    cidstate() {
      return this.modcourse.id.length > 0;
    },
    cnstate() {
      return this.modcourse.name.length > 0;
    },
  },
  methods: {
    validate() {
      let f = 0;
      if (this.modcourse.id === null || this.modcourse.id === '') {
        alert('fill course id');
        f = 1;
      }
      if (this.modcourse.name === null || this.modcourse.name === '') {
        alert('fill course name');
        f = 1;
      }
      if (f === 0) {
        this.$emit('courseupd', this.modcourse);
      }
    },
  },
};
</script>
