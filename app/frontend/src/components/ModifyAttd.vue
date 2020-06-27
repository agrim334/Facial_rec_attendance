<template>
  <div id="modify-form">
    <form @submit.prevent="validate">
    <label>Prof/TA ID</label>
    <input type="text" placeholder = "Enter New mid" v-model = 'modattd.mid'/>
    <br>

    <label>Student ID</label>
    <input type="text" placeholder = "Enter New Student ID" v-model = 'modattd.sid'/>
    <br>

    <label>Course ID</label>
    <input type="text" placeholder = "Enter new Course ID" v-model = 'modattd.cid'/>
    <br>

    <label>TimeStamp(Date of class) </label>
    <input type="text" placeholder = "Enter new Timestamp" v-model = 'modattd.time'/>
    <br>

    <input type="submit" value="Modify attd" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'ModifyAttdForm',
  props: { attdrec: Array },
  data() {
    return {
      modattd: {
        mid: this.attdrec.taid || this.attdrec.fid,
        sid: this.attdrec.sid,
        cid: this.attdrec.cid,
        time: this.attdrec.time,
      },
    };
  },
  methods: {
    validate() {
      let f = 0;
      if (this.modattd.mid === null || this.modattd.mid === '') {
        f = 1;
      }
      if (this.modattd.sid === null || this.modattd.sid === '') {
        f = 1;
      }
      if (this.modattd.cid === null || this.modattd.cid === '') {
        f = 1;
      }
      if (this.modattd.time === null || this.modattd.time === '') {
        f = 1;
      }
      if (f === 0) {
        this.$emit('attdupd', this.modattd);
      }
    },
  },
};
</script>
