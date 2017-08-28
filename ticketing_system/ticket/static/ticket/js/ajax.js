/**
 * Created by Felix-Urtubia on 28-08-17.
 */

$( document ).ready(function() {
   $( ".notificacion").click(function ( event ) {
       $( this ).hide("slow");
       event.preventDefault()
   });
});