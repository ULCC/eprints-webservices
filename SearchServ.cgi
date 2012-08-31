#!/usr/bin/perl

package SearchServ; 

use EPrints; 
use EPrints::DataObj::EPrint; 

sub searchEprint 
    { 
    # input keywords and list fieldes for search
#    my( $self, $key, @fields) = @_;
    my( $self, $key, $fields) = @_;
    
#my $test2=  join(',',\@fields);

    # start ssesion Eprints
    my $session = new EPrints::Session; 
    exit( 0 ) unless( defined $session );
    my $ds = $session->get_repository->get_dataset( "archive" ); 

    # Create search expression
    my $search = new EPrints::Search(
        session => $session, 
	dataset => $ds, 
	custom_order => 'title' );

##############work##################
#$search->add_field(
#    [                                                                       
#	$ds->get_field('type')
#    ],                                                                      
#       $key,                                                        
#      "IN",                                             
#     "ALL" ); 
#####################################


my @ListFields=@{$fields};                                              
                                                            
my $count=@ListFields;                                                 
                                                            
my $i=0;                                                               
    while ($i<$count)                                                  
    {                                                                  
     $st=$st."\$ds->get_field(".@ListFields[$i]."),";            
     $i++;                                                             
     }                                                                 
my $query="\$search->add_field( [".$st."],".$key.",'IN','ANY')".';';     
eval ($query);  

     

# Make search
my $list = $search->perform_search; 

# Modify result for return
my @result=();
# Map function to each result
$list->map( 
	        sub {  
                my( $session, $dataset, $eprint ) = @_; 
                push @result, $eprint->get_id;
	        }
	); 
$list->dispose(); 

# Return result

my $listid=SOAP::Data->name('id')->type('ListOfID')->value(\@result); 
#my $test=SOAP::Data->name('test')->value(\@fields); 

return ($listid);	
	
# Tidy up 
$list->dispose();

# End session   
$session->terminate();  
}

package main;

use SOAP::Lite +trace;
use SOAP::Transport::HTTP;

SOAP::Transport::HTTP::CGI
->dispatch_to( 'SearchServ')
->handle;

1;
