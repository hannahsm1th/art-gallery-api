from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
from artgallery.groups import GroupPermissions
from django.db import DatabaseError
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer, OpenApiResponse
from artworks.models import Artwork
from artworks.serializers import ArtworkSerializer


class ListArtworks(APIView):
    """
    View to list all artworks in the system from model: `artworks.Artworks`.

    * Requires basic authentication.
    * Only users with accounts can view all artworks
    * Only staff and managers are able to update or create artworks.
    * Only managers can delete artworks
    """
    
    authentication_classes = [authentication.BasicAuthentication]
    
    @extend_schema(
        examples=[
            OpenApiExample(
                'Returned data',
                status_codes=['200'],
                value =
                    [
                        {
                            "id": 1,
                            "title": "Something More #1",
                            "image": "/data/images/image1.png",
                            "thumbnail": "/data/thumbnails/image1thumb.png",
                            "date_start": 1989,
                            "date_end": 1989,
                            "place_of_origin": "Albury",
                            "dimensions": "frame 111 x 141 x 3.2cm",
                            "medium_display": "cibachrome print, framed",
                            "provenance_text": "The nine images in Something More tell an ambiguous tale of a young woman's longing for 'something more', a quest which brings dashed hopes and the loss of innocence. With its staged theatricality and storyboard framing, the series has been described by critic Ingrid Perez as 'a collection of scenes from a film that was never made'. While the film may never have been made, we recognise its components from a shared cultural memory of B-grade cinema and pulp fiction, from which Moffatt has drawn this melodrama. The 'scenes' can be displayed in any order - in pairs, rows or as a grid - and so their storyline is not fixed, although we piece together the arc from naïve country girl to fallen woman abandoned on the roadside in whatever arrangement they take. Moffatt capitalises on the cinematic device of montage, mixing together continuous narrative, flashbacks, cutaways, close-ups and memory or dream sequences, to structure the series, and relies on our knowledge of these devices to make sense and meaning out of the assemblage. Something More was made while Moffatt was artist-in-residence at Albury Regional Art Centre in May 1989, and was produced in conjunction with staff and students of the photography department at the Centre for Visual Arts Murray Campus of Charles Sturt University, the artists of the Link Access studio and the general community of Albury Wodonga. Moffatt 'stars' as the beautiful ingénue in the cheongsam, and conjures the stifling atmosphere of small-town life in the cane fields of her native Queensland through vividly painted sets. The pantomime feeling of the series is amplified by the stereotypical characters of the trashy blonde and the Chinese boy-next-door who feature alongside her, and the lush colour saturation of the Cibachrome images. Something More is the first of Moffatt's photographic series which demonstrates all of the elements that have made her work so acclaimed: its theatrical staginess, its references to film, art and photographic history and issues of race and gender.",
                            "is_public_domain": False,
                            "latitude": -33.859964214346284,
                            "longitude": 151.20910207195533,
                            "department": "Photography",
                            "artist_id": 1,
                            "artist_title": "Tracey Moffatt",
                            "created_date": "2022-10-12T03:10:30.191000Z",
                            "last_modified": "2022-10-13T02:14:47.212000Z",
                            "on_display": True
                        },
                        {
                            "id": 2,
                            "title": "The Royal Tour 16, 2020",
                            "image": "/data/images/image1_MYUuImU.png",
                            "thumbnail": "/data/thumbnails/image1thumb_VuP4GiM.png",
                            "date_start": 2020,
                            "date_end": 2020,
                            "place_of_origin": "Alice Springs",
                            "dimensions": "frame 43.3 x 53.1cm",
                            "medium_display": "acrylic on found book pages, framed",
                            "provenance_text": "Vincent Namatjira sourced the material for The Royal Tour from op-shops in Alice Springs, Northern Territory. During the lockdowns for remote community members in the Northern Territory as a result of the COVID-19 pandemic, he was unable to work in his studio. He devised the idea of working directly onto the pages of the found source material, which included magazines, books and other mass-produced paper works featuring the British royal family. This meant he was able to paint at a domestic size, at home in isolation. The artist states that whenever he paints powerful figures - politicians, world leaders or members of the royal family, for example - he is attempting to disrupt or take away their power. He often does this by placing the figures on Aboriginal land, out of their comfort zone, where they are not considered leaders but are viewed as just another visitor. He will also often place himself in the work, in “a mischievous self-portrait, using a bit of cheeky humour kind of as an equaliser - to put everyone on the same level.”[1]  There are some synchronicities with the British monarchy and the Namatjira family. While researching the Namatjira family history, Vincent came to learn that his great-grandfather, the renowned artist Albert Namatjira (1902-1959) had met Queen Elizabeth II when she toured Australia in 1954. It was at this time that he had bestowed upon him the Coronation Medal, a commemorative personal souvenir awarded by the Queen to particularly noteworthy Commonwealth subjects. The British royal family and the Coronation Medal are seen by the artist as symbolic of wealth and power, able to bestow social validation upon those who were considered part of the lower echelons of society. The background of several works in The Royal Tour have been painted in a stylistically similar way tothe work of the artist's great-grandfather. It's a sincere homage to Albert Namatjira's artistic technique, which we now know revealed connections to his custodial Country. The washed, confidently depicted backdrops are also a tribute to the artists - many of whom are related to Vincent Namatjira - at the Iltja Ntjarra (Many Hands) Art Centre, who continue the artistic legacy of Albert Namatjira in their depictions of Country. Vincent's Namatjira's work can be contextualised within a broader artistic framework of humorous political representations in Australian contemporary art. Similar to newspaper cartoons with their leaning towards political satire, his work effortlessly captures a particular generational critique of those who have felt marginalised from the possibility of participating in or influencing sovereignty over their own lives.",
                            "is_public_domain": False,
                            "latitude": -33.859964214346284,
                            "longitude": 151.20910207195533,
                            "department": "Painting",
                            "artist_id": 2,
                            "artist_title": "Vincent Namatjira",
                            "created_date": "2022-10-12T03:59:35.243000Z",
                            "last_modified": "2022-10-12T03:59:35.243000Z",
                            "on_display": True
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the list of all artworks.')
        }
    )
    def get(self, request, format=None):
        """
        Return a list of all artworks.
        * Only users are able to access this view.
        """
        auth_denied = GroupPermissions.UsersOnly(request.user.role, 'view all artworks')
        if auth_denied is None:
            artworks = Artwork.objects.all()
            title = request.GET.get('title', None)
            if title is not None:
                artworks = artworks.filter(title__icontains=title)
            artworks_serializer = ArtworkSerializer(artworks, many=True)
            return Response(artworks_serializer.data)
        else:
            return auth_denied

    @extend_schema(
        examples=[
            OpenApiExample(
                'Successful creation',
                status_codes=['201'],
                value =
                {
                    "title": "Untitled (PSM), 2014",
                    "image": 'null',
                    "thumbnail": 'null',
                    "date_start": 2014,
                    "date_end": 2015,
                    "place_of_origin": "Sydney",
                    "dimensions": "frame 190.5 x 190 x 3.5cm",
                    "medium_display": "oil and archival glue on linen",
                    "provenance_text": "Daniel Boyd's work is concerned with the reinterpretation of Aboriginal and Australian-European history. From the ethics of colonisation to a more personal engagement with family history, his work explores ideas of time and memory, drawing on imagery that has personal, cultural and art-historical significance. A recurring motif in Boyd's painting practice since 2011 is the use of resin dots that he places over a painted image, which is then overlaid with black pigment, resulting in a constellation of semi-transparent 'lenses' that partially reveal the underlying image. Obscured in veiled darkness, these contemplative and intriguing paintings rendered in a tonal greyscale speak of incomplete histories and multiplicities of perspectives, encouraging the viewer to visually and intellectually fill in the gaps. Untitled (PSM) is part of a series of paintings titled History is Made at Night (Kochi) produced by Boyd specifically for the Kochi-Muziris Biennale in Kochi, India in 2014. The four works in this series explore narratives around the fifteenth-century maritime 'age of discovery' and include Untitled (ZVC), a reworking of an 1898 etching of a painting of Portuguese explorer Vasco da Gama; Untitled (KC) 1 and Untitled (KC) 2, renderings of eleventh-century gold coins of the Kilwa Sultanate in East Africa found off the coast of Arnhem Land; and Untitled (PSM), a celestial navigation chart based on a traditional navigational Polynesian star map. These works collectively touch on notions of early trade and exploration and their associated complex and uneasy histories. These narratives have a personal resonance for Boyd, whose paternal great-great-grandfather was brought from Pentecost Island in Vanuatu to Queensland as a slave to work on the cane fields. History is Made at Night (Kochi) follows on from Boyd's exhibitions New Hebrides (2013) and Pineapples in the Pacific (2014) at Roslyn Oxley9 Gallery, Sydney featuring a series of paintings exploring similar ideas focused on Vanuatu.",
                    "is_public_domain": False,
                    "latitude": -33.859964214346284,
                    "longitude": 151.20910207195533,
                    "department": "Painting",
                    "artist_id": 3,
                    "artist_title": "Daniel Boyd",
                    "on_display": False
                },
            ),
            OpenApiExample(
                'Missing data in the request',
                status_codes=['400'],
                value =
                {
                    "image": [
                        "No file was submitted."
                    ],
                    "thumbnail": [
                        "No file was submitted."
                    ],
                    "place_of_origin": [
                        "This field is required."
                    ]
                },
            )
        ],
        request={
            'multipart/form-data': ArtworkSerializer
        },
        responses={
            201: OpenApiResponse(response=int, description='Successful creation will return the input data.'),
            400: OpenApiResponse(response=int, description='Missing data, will return bad request and details about required inputs.'),
        }
    )
    def post(self, request, format=None):
        """
        Add an artwork to the list of all artworks.

        * Only managers or staff can add artworks
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'add new artworks')
        if auth_denied is None:
            artwork_serializer = ArtworkSerializer(data=request.data)
            if artwork_serializer.is_valid():
                artwork_serializer.save()
                return Response(artwork_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(artwork_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return auth_denied

    @extend_schema( 
        responses={
            204: OpenApiResponse(response=int, description='Returns nothing on successful deletion.')
        }
    )
    def delete(self, request, format=None):
        """
        Delete all artworks.

        * Only managers can do this action
        """
        auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'delete all artworks')
        if auth_denied is None:
            count = Artwork.objects.all().delete()
            return Response({'message': '{} artworks were deleted.'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
        else:
            return auth_denied


class ListArtworkDetail(APIView):
    """
    View to list a single artwork in the system.

    * Requires basic authentication.
    * Only users with accounts can view artworks
    * Only managers or staff can update an artwork
    * Only managers can delete an artwork
    """
    
    authentication_classes = [authentication.BasicAuthentication]

    @extend_schema(
        examples=[
            OpenApiExample(
                'Returned data for the requested artwork.',
                status_codes=['200'],
                value =
                    [
                        {
                            "id": 1,
                            "title": "Something More #1",
                            "image": "/data/images/image1.png",
                            "thumbnail": "/data/thumbnails/image1thumb.png",
                            "date_start": 1989,
                            "date_end": 1989,
                            "place_of_origin": "Albury",
                            "dimensions": "frame 111 x 141 x 3.2cm",
                            "medium_display": "cibachrome print, framed",
                            "provenance_text": "The nine images in Something More tell an ambiguous tale of a young woman's longing for 'something more', a quest which brings dashed hopes and the loss of innocence. With its staged theatricality and storyboard framing, the series has been described by critic Ingrid Perez as 'a collection of scenes from a film that was never made'. While the film may never have been made, we recognise its components from a shared cultural memory of B-grade cinema and pulp fiction, from which Moffatt has drawn this melodrama. The 'scenes' can be displayed in any order - in pairs, rows or as a grid - and so their storyline is not fixed, although we piece together the arc from naïve country girl to fallen woman abandoned on the roadside in whatever arrangement they take. Moffatt capitalises on the cinematic device of montage, mixing together continuous narrative, flashbacks, cutaways, close-ups and memory or dream sequences, to structure the series, and relies on our knowledge of these devices to make sense and meaning out of the assemblage. Something More was made while Moffatt was artist-in-residence at Albury Regional Art Centre in May 1989, and was produced in conjunction with staff and students of the photography department at the Centre for Visual Arts Murray Campus of Charles Sturt University, the artists of the Link Access studio and the general community of Albury Wodonga. Moffatt 'stars' as the beautiful ingénue in the cheongsam, and conjures the stifling atmosphere of small-town life in the cane fields of her native Queensland through vividly painted sets. The pantomime feeling of the series is amplified by the stereotypical characters of the trashy blonde and the Chinese boy-next-door who feature alongside her, and the lush colour saturation of the Cibachrome images. Something More is the first of Moffatt's photographic series which demonstrates all of the elements that have made her work so acclaimed: its theatrical staginess, its references to film, art and photographic history and issues of race and gender.",
                            "is_public_domain": False,
                            "latitude": -33.859964214346284,
                            "longitude": 151.20910207195533,
                            "department": "Photography",
                            "artist_id": 1,
                            "artist_title": "Tracey Moffatt",
                            "created_date": "2022-10-12T03:10:30.191000Z",
                            "last_modified": "2022-10-13T02:14:47.212000Z",
                            "on_display": True
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the requested artwork.'),
            404: OpenApiResponse(response=int, description='The given id does not match any artwork is in the database.'),
        }
    )    
    def get(self, request, pk):
        """
        Return an artwork.
        """
        auth_denied = GroupPermissions.UsersOnly(request.user.role, 'view all artworks')
        if auth_denied is None:
            try:
                artwork = Artwork.objects.get(pk=pk)
            except Artwork.DoesNotExist:
                return Response({'message': 'The artwork does not exist'}, status=status.HTTP_404_NOT_FOUND)
            artwork_serializer = ArtworkSerializer(artwork)
            return Response(artwork_serializer.data)
        else:
            return auth_denied
    
    @extend_schema(
        examples=[
            OpenApiExample(
                'Successful update',
                status_codes=['201'],
                value =
                    [
                        {
                            "id": 1,
                            "title": "Something More #1",
                            "image": "/data/images/image1.png",
                            "thumbnail": "/data/thumbnails/image1thumb.png",
                            "date_start": 1989,
                            "date_end": 1989,
                            "place_of_origin": "Albury",
                            "dimensions": "frame 111 x 141 x 3.2cm",
                            "medium_display": "cibachrome print, framed",
                            "provenance_text": "The nine images in Something More tell an ambiguous tale of a young woman's longing for 'something more', a quest which brings dashed hopes and the loss of innocence. With its staged theatricality and storyboard framing, the series has been described by critic Ingrid Perez as 'a collection of scenes from a film that was never made'. While the film may never have been made, we recognise its components from a shared cultural memory of B-grade cinema and pulp fiction, from which Moffatt has drawn this melodrama. The 'scenes' can be displayed in any order - in pairs, rows or as a grid - and so their storyline is not fixed, although we piece together the arc from naïve country girl to fallen woman abandoned on the roadside in whatever arrangement they take. Moffatt capitalises on the cinematic device of montage, mixing together continuous narrative, flashbacks, cutaways, close-ups and memory or dream sequences, to structure the series, and relies on our knowledge of these devices to make sense and meaning out of the assemblage. Something More was made while Moffatt was artist-in-residence at Albury Regional Art Centre in May 1989, and was produced in conjunction with staff and students of the photography department at the Centre for Visual Arts Murray Campus of Charles Sturt University, the artists of the Link Access studio and the general community of Albury Wodonga. Moffatt 'stars' as the beautiful ingénue in the cheongsam, and conjures the stifling atmosphere of small-town life in the cane fields of her native Queensland through vividly painted sets. The pantomime feeling of the series is amplified by the stereotypical characters of the trashy blonde and the Chinese boy-next-door who feature alongside her, and the lush colour saturation of the Cibachrome images. Something More is the first of Moffatt's photographic series which demonstrates all of the elements that have made her work so acclaimed: its theatrical staginess, its references to film, art and photographic history and issues of race and gender.",
                            "is_public_domain": False,
                            "latitude": -33.859964214346284,
                            "longitude": 151.20910207195533,
                            "department": "Photography",
                            "artist_id": 1,
                            "artist_title": "Tracey Moffatt",
                            "created_date": "2022-10-12T03:10:30.191000Z",
                            "last_modified": "2022-10-13T02:14:47.212000Z",
                            "on_display": True
                        }
                    ],
            ),
            OpenApiExample(
                'Missing data in the request',
                status_codes=['400'],
                value =
                {
                    "sortTitle": [
                        "This field is required."
                    ]
                },
            )
        ],
        request={
            'multipart/form-data': ArtworkSerializer
        },
        responses={
            201: OpenApiResponse(response=int, description='Successful update will return the input data.'),
            400: OpenApiResponse(response=int, description='Missing data will return bad request and details about required inputs.'),
        }
    )   
    def put(self, request, pk):
        """
        Update an artwork.
        * Only managers or staff can update an artwork
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'update an artwork')
        if auth_denied is None:
            try:
                artwork = Artwork.objects.get(pk=pk)
            except Artwork.DoesNotExist:
                return Response({'message': 'The artwork does not exist'}, status=status.HTTP_404_NOT_FOUND)
            artwork_serializer = ArtworkSerializer(artwork, data = request.data, partial=True)
            if artwork_serializer.is_valid():
                artwork_serializer.save()
                return Response(artwork_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(artwork_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return auth_denied

    @extend_schema(
        responses={
            204: OpenApiResponse(response=int, description='Returns nothing on successful deletion.'),
            404: OpenApiResponse(response=int, description='The given id does not match any artwork is in the database.'),
        }
    )
    def delete(self, request, pk):
        """
        Delete an artwork.
        * Only managers can delete an artwork
        """
        auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'delete artworks')
        if auth_denied is None:
            try:
                artwork = Artwork.objects.get(pk=pk)
            except Artwork.DoesNotExist:
                return Response({'message': 'The artwork does not exist'}, status=status.HTTP_404_NOT_FOUND)
            artwork.delete()
            return Response({'message': 'Artwork was deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return auth_denied


class ListDisplayedArtworks(APIView):
    """
    View to list the artworks that are currrently on display.

    * Allows anonymous access
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        examples=[
            OpenApiExample(
                'Returned data',
                status_codes=['200'],
                value =
                    [
                        {
                            "id": 1,
                            "title": "Something More #1",
                            "image": "/data/images/image1.png",
                            "thumbnail": "/data/thumbnails/image1thumb.png",
                            "date_start": 1989,
                            "date_end": 1989,
                            "place_of_origin": "Albury",
                            "dimensions": "frame 111 x 141 x 3.2cm",
                            "medium_display": "cibachrome print, framed",
                            "provenance_text": "The nine images in Something More tell an ambiguous tale of a young woman's longing for 'something more', a quest which brings dashed hopes and the loss of innocence. With its staged theatricality and storyboard framing, the series has been described by critic Ingrid Perez as 'a collection of scenes from a film that was never made'. While the film may never have been made, we recognise its components from a shared cultural memory of B-grade cinema and pulp fiction, from which Moffatt has drawn this melodrama. The 'scenes' can be displayed in any order - in pairs, rows or as a grid - and so their storyline is not fixed, although we piece together the arc from naïve country girl to fallen woman abandoned on the roadside in whatever arrangement they take. Moffatt capitalises on the cinematic device of montage, mixing together continuous narrative, flashbacks, cutaways, close-ups and memory or dream sequences, to structure the series, and relies on our knowledge of these devices to make sense and meaning out of the assemblage. Something More was made while Moffatt was artist-in-residence at Albury Regional Art Centre in May 1989, and was produced in conjunction with staff and students of the photography department at the Centre for Visual Arts Murray Campus of Charles Sturt University, the artists of the Link Access studio and the general community of Albury Wodonga. Moffatt 'stars' as the beautiful ingénue in the cheongsam, and conjures the stifling atmosphere of small-town life in the cane fields of her native Queensland through vividly painted sets. The pantomime feeling of the series is amplified by the stereotypical characters of the trashy blonde and the Chinese boy-next-door who feature alongside her, and the lush colour saturation of the Cibachrome images. Something More is the first of Moffatt's photographic series which demonstrates all of the elements that have made her work so acclaimed: its theatrical staginess, its references to film, art and photographic history and issues of race and gender.",
                            "is_public_domain": False,
                            "latitude": -33.859964214346284,
                            "longitude": 151.20910207195533,
                            "department": "Photography",
                            "artist_id": 1,
                            "artist_title": "Tracey Moffatt",
                            "created_date": "2022-10-12T03:10:30.191000Z",
                            "last_modified": "2022-10-13T02:14:47.212000Z",
                            "on_display": True
                        },
                        {
                            "id": 2,
                            "title": "The Royal Tour 16, 2020",
                            "image": "/data/images/image1_MYUuImU.png",
                            "thumbnail": "/data/thumbnails/image1thumb_VuP4GiM.png",
                            "date_start": 2020,
                            "date_end": 2020,
                            "place_of_origin": "Alice Springs",
                            "dimensions": "frame 43.3 x 53.1cm",
                            "medium_display": "acrylic on found book pages, framed",
                            "provenance_text": "Vincent Namatjira sourced the material for The Royal Tour from op-shops in Alice Springs, Northern Territory. During the lockdowns for remote community members in the Northern Territory as a result of the COVID-19 pandemic, he was unable to work in his studio. He devised the idea of working directly onto the pages of the found source material, which included magazines, books and other mass-produced paper works featuring the British royal family. This meant he was able to paint at a domestic size, at home in isolation. The artist states that whenever he paints powerful figures - politicians, world leaders or members of the royal family, for example - he is attempting to disrupt or take away their power. He often does this by placing the figures on Aboriginal land, out of their comfort zone, where they are not considered leaders but are viewed as just another visitor. He will also often place himself in the work, in “a mischievous self-portrait, using a bit of cheeky humour kind of as an equaliser - to put everyone on the same level.”[1]  There are some synchronicities with the British monarchy and the Namatjira family. While researching the Namatjira family history, Vincent came to learn that his great-grandfather, the renowned artist Albert Namatjira (1902-1959) had met Queen Elizabeth II when she toured Australia in 1954. It was at this time that he had bestowed upon him the Coronation Medal, a commemorative personal souvenir awarded by the Queen to particularly noteworthy Commonwealth subjects. The British royal family and the Coronation Medal are seen by the artist as symbolic of wealth and power, able to bestow social validation upon those who were considered part of the lower echelons of society. The background of several works in The Royal Tour have been painted in a stylistically similar way tothe work of the artist's great-grandfather. It's a sincere homage to Albert Namatjira's artistic technique, which we now know revealed connections to his custodial Country. The washed, confidently depicted backdrops are also a tribute to the artists - many of whom are related to Vincent Namatjira - at the Iltja Ntjarra (Many Hands) Art Centre, who continue the artistic legacy of Albert Namatjira in their depictions of Country. Vincent's Namatjira's work can be contextualised within a broader artistic framework of humorous political representations in Australian contemporary art. Similar to newspaper cartoons with their leaning towards political satire, his work effortlessly captures a particular generational critique of those who have felt marginalised from the possibility of participating in or influencing sovereignty over their own lives.",
                            "is_public_domain": False,
                            "latitude": -33.859964214346284,
                            "longitude": 151.20910207195533,
                            "department": "Painting",
                            "artist_id": 2,
                            "artist_title": "Vincent Namatjira",
                            "created_date": "2022-10-12T03:59:35.243000Z",
                            "last_modified": "2022-10-12T03:59:35.243000Z",
                            "on_display": True
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the list of all displayed artworks.')
        }
    )        
    def get(self, request, format=None):
        try:
            artworks = Artwork.objects.filter(on_display__in=[True]) #workaround for bug in Django querysets for booleans
        except:
            return Response({'message': 'No artworks are displayed'}, status=status.HTTP_404_NOT_FOUND)
        artwork_serializer = ArtworkSerializer(artworks, many=True)
        return Response(artwork_serializer.data)